"use client"; // Required for Next.js App Router

import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import { TextField, Button, Box, Typography, Container } from "@mui/material";
import { config } from "@/lib/constant";

const Signup = () => {
  const [formData, setFormData] = useState({
    user_name: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const router = useRouter();

  const handleLogin = () => {
    router.push("/login");
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${config.url}/register`, formData);
      if (response.data.statusCode === 201) {
        setError("");
        handleLogin(); // Redirect to login after successful signup
      } else {
        setError(response.data.body.error);
      }
    } catch (error) {
      setError(error.response?.data || "An error occurred");
      console.log("Signup error:", error);
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
          Sign Up
        </Typography>

        <TextField
          label='Name'
          name='user_name'
          fullWidth
          margin='normal'
          value={formData.user_name}
          onChange={handleChange}
        />

        <TextField
          label='Email'
          name='email'
          type='email'
          fullWidth
          margin='normal'
          value={formData.email}
          onChange={handleChange}
        />

        <TextField
          label='Password'
          name='password'
          type='password'
          fullWidth
          margin='normal'
          value={formData.password}
          onChange={handleChange}
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
          onClick={handleSignup}
        >
          Sign Up
        </Button>

        <Typography sx={{ mt: 2 }}>
          Already have an account?{" "}
          <Button color='secondary' onClick={handleLogin}>
            Login
          </Button>
        </Typography>
      </Box>
    </Container>
  );
};

export default Signup;
