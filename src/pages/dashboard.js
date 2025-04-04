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
} from "@mui/material";

import { config } from "@/lib/constant";

const Dashboard = () => {
  const [token, setToken] = useState(null);
  const router = useRouter();
  const [results, setResults] = useState([]);

  const [title, setTitle] = useState("");
  const [artist, setArtist] = useState("");
  const [album, setAlbum] = useState("");
  const [year, setYear] = useState("");
  const [subscribe, setSubscribe] = useState(true);
  const [message, setMessage] = useState("");
  // Fetch user's subscribed music
  const getMusic = async (storedData) => {
    try {
      const response = await axios.get("/api/list", {
        headers: { Authorization: `Bearer ${storedData}` },
      });
      setSubscribe(true);
      if (response.data.error) setResults("No subscription");
      else
        setResults(response.data.message || response.data || "No subscription");
    } catch (error) {
      console.error("Error fetching subscriptions:", error);
    }
  };

  // Handle search request
  const handleSearch = async () => {
    try {
      setResults([]);
      setSubscribe(false);
      const response = await axios.get("/api/search", {
        params: { title, artist, album, year },
        headers: { Authorization: `Bearer ${token}` },
      });
      setResults(response.data);
    } catch (error) {
      console.error("Error searching:", error);
    }
  };

  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    router.push("/login");
  };

  const handleSubscribe = async (music_id) => {
    let response = null;
    if (!subscribe) {
      response = await axios.post(
        "/api/subscribe",
        {
          music_id,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
    } else {
      response = await axios.delete("/api/subscribe", {
        headers: { Authorization: `Bearer ${token}` },
        data: {
          music_id,
        },
      });
    }
    console.log(response);
    setMessage(response.data.message);
    getMusic(localStorage.getItem("token"));
  };

  const handleClose = () => {
    setMessage("");
  };

  useEffect(() => {
    const storedData = localStorage.getItem("token");
    if (storedData) {
      setToken(storedData);
      getMusic(storedData);
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

      {/* Search Form */}
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
        <Button
          variant='contained'
          color='primary'
          onClick={handleSearch}
          sx={{ alignSelf: "center", width: "50%" }}
        >
          Search
        </Button>
      </Box>
      {!results.length && (
        <Typography variant='h6' color='error'>
          Loading...
        </Typography>
      )}
      {/* Results */}
      {typeof results === "string" ? (
        <Typography variant='h6' color='error'>
          {results}
        </Typography>
      ) : (
        <Grid container spacing={3}>
          {results?.map((music) => (
            <Grid item xs={12} sm={6} md={4} key={music.music_id}>
              <Card sx={{ maxWidth: 345 }}>
                <CardMedia
                  component='img'
                  height='200'
                  width='300'
                  image={`data:image/jpeg;base64,${music.img_url}`}
                  alt='Music Cover'
                />
                <CardContent>
                  <Typography variant='h6'>{music.title}</Typography>
                  <Typography color='textSecondary'>
                    {music.year} | {music.artist}
                  </Typography>
                  <Typography variant='body2'>{music.album}</Typography>
                </CardContent>
                <Button onClick={() => handleSubscribe(music.music_id)}>
                  {!subscribe ? "Subscribe" : "Unsubscribe"}
                </Button>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
      <Snackbar
        open={!!message}
        autoHideDuration={6000}
        onClose={handleClose}
        message={message}
        // action={action}
      />
    </Container>
  );
};

export default Dashboard;
