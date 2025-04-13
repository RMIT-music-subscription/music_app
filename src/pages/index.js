import axios from "axios";
import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import {
  AppBar,
  Toolbar,
  Button,
  Typography,
  TextField,
  Card,
  CardContent,
  CardMedia,
  Grid,
  Container,
  Box,
  Snackbar,
  CircularProgress,
} from "@mui/material";

import { config } from "@/lib/constant";

const Dashboard = () => {
  const [token, setToken] = useState(null);
  const router = useRouter();
  const [results, setResults] = useState([]);
  const [username, setUsername] = useState("");
  const [title, setTitle] = useState("");
  const [artist, setArtist] = useState("");
  const [album, setAlbum] = useState("");
  const [year, setYear] = useState("");
  const [subscribe, setSubscribe] = useState(true);
  const [message, setMessage] = useState("");
  const [imgBase64, setImgBase64] = useState({});
  const [loading, setLoading] = useState(false);

  // Fetch user's subscribed music
  const getMusic = async (storedData) => {
    try {
      setLoading(true);
      const response = await axios.post(`${config.url}/list`, {
        token: storedData,
      });

      if (response.data.body) {
        setResults(response.data.body.music);
        setImgBase64(response.data.body.img_base64);
      } else {
        setMessage(response.data.body.error);
      }
      setSubscribe(true);

      setLoading(false);
    } catch (error) {
      setLoading(false);
      console.log("Error fetching subscriptions::", error);
      setMessage(error?.response?.data?.error || "Try again");
    }
  };

  // Handle search request
  const handleSearch = async () => {
    try {
      setLoading(true);
      setResults([]);
      setSubscribe(false);
      const response = await axios.post(`${config.url}/search`, {
        title,
        artist,
        album,
        year,
        token,
      });
      console.log(response, "::");

      if (!response.data.body.error) {
        setResults(response.data.body.music);
        setImgBase64(response.data.body.img_base64);
      } else {
        setMessage(response.data.body.error);
      }

      setLoading(false);
    } catch (error) {
      setLoading(false);
      console.log("Error searching:", error);
      setMessage(error?.response?.data?.error || "Try again");
    }
  };

  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    router.push("/login");
  };

  const handleSubscribe = async (music_id) => {
    try {
      let response = null;
      setLoading(true);
      if (!subscribe) {
        const response = await axios.post(`${config.url}/subscribe`, {
          music_id,
          token,
        });
        console.log(response, "::");

        if (response.data.body) {
          setMessage(response.data.body.message);
        } else {
          setMessage(response.data.body.error);
        }
      } else {
        response = await axios.delete(`${config.url}/subscribe`, {
          data: {
            music_id,
            token,
          },
        });
        console.log(response, "::");
        if (response.data.body) {
          setMessage(response.data.body.message);
        } else {
          setMessage(response.data.body.error);
        }
      }

      setLoading(false);
      getMusic(localStorage.getItem("token"));
    } catch (error) {
      setLoading(false);
      setMessage("Try again");
    }
  };

  const handleClose = () => {
    setMessage("");
  };

  const handleCancel = () => {
    setTitle("");
    setArtist("");
    setAlbum("");
    setYear("");
    getMusic(localStorage.getItem("token"));
  };

  useEffect(() => {
    const storedData = localStorage.getItem("token");
    if (storedData) {
      setUsername(localStorage.getItem("username"));
      setToken(storedData);
      getMusic(storedData);
    } else {
      handleLogout();
    }
  }, []);

  return (
    <Container maxWidth='lg'>
      {/* Navbar */}
      <AppBar position='static'>
        <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
          <Typography variant='h6'>Music Dashboard</Typography>
          <Button color='inherit' onClick={handleLogout}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>

      <Typography variant='h6'>Welcome {username},</Typography>
      <Box
        my={4}
        component='form'
        display='flex'
        flexDirection='column'
        gap={2}
      >
        <TextField
          label='Title'
          variant='outlined'
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          fullWidth
        />
        <TextField
          label='Artist'
          variant='outlined'
          value={artist}
          onChange={(e) => setArtist(e.target.value)}
          fullWidth
        />
        <TextField
          label='Album'
          variant='outlined'
          value={album}
          onChange={(e) => setAlbum(e.target.value)}
          fullWidth
        />
        <TextField
          label='Year'
          variant='outlined'
          value={year}
          onChange={(e) => setYear(e.target.value)}
          fullWidth
        />
        <Box sx={{ display: "flex", justifyContent: "space-evenly" }}>
          <Button
            variant='contained'
            color='primary'
            onClick={handleSearch}
            sx={{ alignSelf: "center", width: "40%" }}
          >
            Search
          </Button>
          <Button
            variant='contained'
            color='primary'
            onClick={handleCancel}
            sx={{ alignSelf: "center", width: "40%" }}
          >
            Reset
          </Button>
        </Box>
      </Box>
      {loading && (
        <Typography variant='h6' color='error'>
          <CircularProgress color='secondary' />
        </Typography>
      )}
      {/* Results */}
      {typeof results === "string" && !loading ? (
        <Typography variant='h6' color='error'>
          {results}
        </Typography>
      ) : (
        <Grid container spacing={3}>
          {results?.map((music) => (
            <Grid item xs={12} sm={6} md={3} key={music.music_id}>
              <Card
                sx={{
                  maxWidth: 300,
                  minHeight: 400,
                  maxHeight: 400,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "start",
                  justifyContent: "space-between",
                }}
              >
                <CardMedia
                  sx={{
                    minWidth: 300,
                    minHeight: 200,
                    maxWidth: 300,
                    maxHeight: 200,
                  }}
                  component='img'
                  image={`data:image/jpeg;base64,${
                    imgBase64[music?.img_url || music?.img]
                  }`}
                  alt='Music Cover'
                />
                <CardContent>
                  <Typography variant='h6' sx={{ color: "darkcyan" }}>
                    {music.title}
                  </Typography>
                  <Typography color='textSecondary'>
                    {music.year} | {music.artist}
                  </Typography>
                  <Typography variant='body2'>{music.album}</Typography>
                </CardContent>
                <Button
                  sx={{ width: "100%" }}
                  variant='contained'
                  onClick={() => handleSubscribe(music.music_id)}
                >
                  <Typography textAlign='center'>
                    {!subscribe ? "Subscribe" : "Remove"}
                  </Typography>
                </Button>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
      <Snackbar
        open={!!message}
        autoHideDuration={3000}
        onClose={handleClose}
        message={message}
      />
    </Container>
  );
};

export default Dashboard;
