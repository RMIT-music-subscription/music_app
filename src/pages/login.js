import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import {
  TextField,
  Button,
  Box,
  Typography,
  Container,
  Divider,
} from "@mui/material";
import { config } from "@/lib/constant";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleLogin = async () => {
    try {
      const response = await axios.post(`${config.url}/music_login`, {
        email,
        password,
      });

      if (response.data.statusCode === 201) {
        setError("");
        localStorage.setItem("token", response.data.body.token);
        localStorage.setItem("username", response.data.body.userName);
        router.push("/dashboard");
      } else {
        setError(response.data.body.error);
      }
    } catch (error) {
      setError(error.response?.data || "Login failed");
      console.error("Login error", error);
    }
  };

  return (
    <Container maxWidth='sm' sx={{ mt: 10 }}>
      <Box
        display='flex'
        flexDirection='column'
        alignItems='center'
        p={4}
        boxShadow={3}
        borderRadius={2}
        bgcolor='white'
      >
        <Typography variant='h4' gutterBottom>
          Login
        </Typography>

        <TextField
          label='Email'
          type='email'
          fullWidth
          margin='normal'
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <TextField
          label='Password'
          type='password'
          fullWidth
          margin='normal'
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {error && (
          <Typography color='error' sx={{ mt: 1 }}>
            {error}
          </Typography>
        )}

        <Button
          variant='contained'
          color='primary'
          fullWidth
          sx={{ mt: 2 }}
          onClick={handleLogin}
        >
          Login
        </Button>

        <Divider sx={{ my: 3, width: "100%" }} />

        <Button
          color='secondary'
          fullWidth
          onClick={() => router.push("/signup")}
        >
          Create an account
        </Button>
      </Box>
    </Container>
  );
};

export default Login;
