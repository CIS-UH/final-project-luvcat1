const express = require('express');
const router = express.Router();
const axios = require('axios');

const API = "http://localhost:5000";

// MEMBERS

// CREATE
router.post('/members/add', async (req, res) => {
    await axios.post(`${API}/members`, req.body);
    res.redirect('/');
});

// READ
// router.get('/', async (req, res) => {
//    const members = await axios.get(`${API}/members`);
//    res.render('index', { members: members.data });
//});

// UPDATE
router.post('/members/update/:id', async (req, res) => {
    await axios.put(`${API}/members/${req.params.id}`, req.body);
    res.redirect('/');
});

// DELETE
router.post('/members/delete/:id', async (req, res) => {
    await axios.delete(`${API}/members/${req.params.id}`);
    res.redirect('/');
});

// EVENTS

// CREATE
router.post('/events/add', async (req, res) => {
    await axios.post(`${API}/events`, req.body);
    res.redirect('/');
});

// READ
router.get('/', async (req, res) => {
  try {
    const [membersRes, eventsRes, registrationsRes] = await Promise.all([
        axios.get(`${API}/members`),
        axios.get(`${API}/events`),
        axios.get(`${API}/registrations`)
    ]);

    res.render('index', {
        members: membersRes.data,
        events: eventsRes.data,
        registrations: registrationsRes.data
    });
  } catch (err) {
    console.error("Error fetching data:", err.message);
    // Provide defaults so the page doesn't crash if one API call fails
    res.render('index', { members: [], events: [], registrations: [] });
  }
});

// UPDATE
router.post('/events/update/:id', async (req, res) => {
    await axios.put(`${API}/events/${req.params.id}`, req.body);
    res.redirect('/');
});

// DELETE
router.post('/events/delete/:id', async (req, res) => {
    await axios.delete(`${API}/events/${req.params.id}`);
    res.redirect('/');
});

// REGISTRATIONS

// CREATE
router.post('/registrations/add', async (req, res) => {
    await axios.post(`${API}/registrations`, req.body);
    res.redirect('/');
});

// DELETE
router.post('/registrations/delete/:id', async (req, res) => {
    await axios.delete(`${API}/registrations/${req.params.id}`);
    res.redirect('/');
});

module.exports = router;