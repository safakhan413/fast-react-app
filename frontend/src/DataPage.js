// src/DataPage.js

import React, { useState } from 'react';
import axios from 'axios';
import {
  Container, TextField, Button, Select, InputLabel, FormControl,
  Typography, Box, TableContainer, Table, TableHead, TableRow,
  TableCell, TableBody, Paper, Alert, MenuItem,
} from '@mui/material';
import { CSVLink } from 'react-csv';
import LoadingSpinner from './components/LoadingSpinner';
import { useNavigate } from 'react-router-dom';

function DataPage() {
  const navigate = useNavigate();

  // State variables
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [parameter, setParameter] = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([]);
  const [csvData, setCsvData] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/');
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setErrorMessage('');

    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      alert('Session expired. Please log in again.');
      navigate('/');
      return;
    }

    const params = {
      start_time: Math.floor(new Date(startTime).getTime() / 1000),
      end_time: Math.floor(new Date(endTime).getTime() / 1000),
      parameter: parameter || null,
    };

    try {
      const response = await axios.get('http://localhost:8000/users/', {
        params,
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      setData(response.data);

      // Process data for CSV
      const processedData = response.data.map((row) => ({
        id: row.id,
        userId: row.userId,
        originationTime: new Date(row.originationTime * 1000).toLocaleString(),
        clusterId: row.clusterId,
        phones: row.phones.map((p) => p.identifier).join('; '),
        voicemails: row.voicemails.map((v) => v.identifier).join('; '),
      }));
      setCsvData(processedData);

    } catch (error) {
      console.error('Error fetching data:', error);
      setErrorMessage('Failed to fetch data. Please check your inputs.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box mt={4}>
        <Typography variant="h4" gutterBottom>
          Data Viewer
        </Typography>
        <Button variant="outlined" color="secondary" onClick={handleLogout} sx={{ mb: 2 }}>
          Logout
        </Button>

        <Box component="form" onSubmit={handleSubmit} sx={{ mb: 4 }}>
          <Box display="flex" flexWrap="wrap" gap={2} alignItems="center">
            <TextField
              label="Start Time"
              type="datetime-local"
              value={startTime}
              onChange={(e) => setStartTime(e.target.value)}
              InputLabelProps={{ shrink: true }}
              required
            />
            <TextField
              label="End Time"
              type="datetime-local"
              value={endTime}
              onChange={(e) => setEndTime(e.target.value)}
              InputLabelProps={{ shrink: true }}
              required
            />
            <FormControl sx={{ minWidth: 150 }}>
              <InputLabel>Parameter</InputLabel>
              <Select
                value={parameter}
                label="Parameter"
                onChange={(e) => setParameter(e.target.value)}
                required
              >
                <MenuItem value=""><em>None</em></MenuItem>
                <MenuItem value="user_id">User ID</MenuItem>
                <MenuItem value="phone">Phone Number</MenuItem>
                <MenuItem value="voicemail">Voicemail</MenuItem>
                <MenuItem value="cluster">Cluster</MenuItem>
              </Select>
            </FormControl>
            <Button variant="contained" color="primary" type="submit">
              Fetch Data
            </Button>
          </Box>
        </Box>

        {errorMessage && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {errorMessage}
          </Alert>
        )}

        {loading && <LoadingSpinner />}

        {!loading && data.length > 0 && (
          <>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>ID</TableCell>
                    <TableCell>User ID</TableCell>
                    <TableCell>Origination Time</TableCell>
                    <TableCell>Cluster ID</TableCell>
                    <TableCell>Phones</TableCell>
                    <TableCell>Voicemails</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {data.map((row) => (
                    <TableRow key={row.id}>
                      <TableCell>{row.id}</TableCell>
                      <TableCell>{row.userId}</TableCell>
                      <TableCell>{new Date(row.originationTime * 1000).toLocaleString()}</TableCell>
                      <TableCell>{row.clusterId}</TableCell>
                      <TableCell>{row.phones.map((p) => p.identifier).join(', ')}</TableCell>
                      <TableCell>{row.voicemails.map((v) => v.identifier).join(', ')}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>

            <Button variant="contained" color="primary" sx={{ mt: 2 }}>
              <CSVLink
                data={csvData}
                filename="data.csv"
                headers={[
                  { label: 'ID', key: 'id' },
                  { label: 'User ID', key: 'userId' },
                  { label: 'Origination Time', key: 'originationTime' },
                  { label: 'Cluster ID', key: 'clusterId' },
                  { label: 'Phones', key: 'phones' },
                  { label: 'Voicemails', key: 'voicemails' },
                ]}
                style={{ color: '#fff', textDecoration: 'none' }}
              >
                Download CSV
              </CSVLink>
            </Button>
          </>
        )}
      </Box>
    </Container>
  );
}

export default DataPage;
