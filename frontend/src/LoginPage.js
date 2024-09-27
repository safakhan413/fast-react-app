// src/LoginPage.js

import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Container, TextField, Button, Typography, Box } from '@mui/material';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate(); // Ensure useNavigate is imported and used correctly

  const handleLogin = async (event) => {
    event.preventDefault(); // Prevent the default form submission behavior
    const data = new URLSearchParams();
    data.append('username', username);
    data.append('password', password);

    try {
      const response = await axios.post('http://localhost:8000/token', data, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      // Log the response to check if access_token is present
      console.log('Login response:', response);

      const { access_token } = response.data;
      if (access_token) {
        localStorage.setItem('access_token', access_token);
        navigate('/data'); // Redirect to the data page
      } else {
        alert('Login failed: No access token received.');
      }
    } catch (error) {
      console.error('Login error:', error);
      alert('Login failed. Please check your username and password.');
    }
  };

  return (
    <Container maxWidth="sm">
      <Box mt={8}>
        <Typography variant="h4" align="center" gutterBottom>
          Login
        </Typography>
        <Box component="form" onSubmit={handleLogin}>
          <TextField
            fullWidth
            label="Username"
            margin="normal"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <TextField
            fullWidth
            label="Password"
            margin="normal"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <Button
            fullWidth
            variant="contained"
            color="primary"
            sx={{ mt: 2 }}
            type="submit"
          >
            Login
          </Button>
        </Box>
      </Box>
    </Container>
  );
}

export default LoginPage;
