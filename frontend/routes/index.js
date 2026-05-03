const express = require('express');
const router = express.Router();
const axios = require('axios');

const API = "http://localhost:5000";

// ── MEMBERS ──────────────────────────────────────────────

// CREATE
router.post('/members/add', async (req, res) => {
    try {
        await axios.post(`${API}/members`, req.body);
    } catch (err) {
        console.error('Add member error:', err.message);
    }
    res.redirect('/');
});

// UPDATE
router.post('/members/update/:id', async (req, res) => {
    try {
        await axios.put(`${API}/members/${req.params.id}`, req.body);
    } catch (err) {
        console.error('Update member error:', err.message);
    }
    res.redirect('/');
});

// DELETE
router.post('/members/delete/:id', async (req, res) => {
    try {
        await axios.delete(`${API}/members/${req.params.id}`);
    } catch (err) {
        console.error('Delete member error:', err.message);
    }
    res.redirect('/');
});

// ── EVENTS ───────────────────────────────────────────────

// CREATE — rejects duplicate dates
router.post('/events/add', async (req, res) => {
    try {
        const eventsRes = await axios.get(`${API}/events`);
        const duplicate = eventsRes.data.find(function(e) {
            return e.date === req.body.date;
        });
        if (duplicate) {
            console.warn('Duplicate date rejected:', req.body.date);
            return res.redirect('/?error=duplicate_date');
        }
        await axios.post(`${API}/events`, req.body);
    } catch (err) {
        console.error('Add event error:', err.message);
    }
    res.redirect('/');
});

// UPDATE — rejects duplicate dates (ignores the event being edited)
router.post('/events/update/:id', async (req, res) => {
    try {
        const eventsRes = await axios.get(`${API}/events`);
        const duplicate = eventsRes.data.find(function(e) {
            return e.date === req.body.date && e.id !== parseInt(req.params.id);
        });
        if (duplicate) {
            console.warn('Duplicate date rejected on update:', req.body.date);
            return res.redirect('/?error=duplicate_date');
        }
        await axios.put(`${API}/events/${req.params.id}`, req.body);
    } catch (err) {
        console.error('Update event error:', err.message);
    }
    res.redirect('/');
});

// DELETE
router.post('/events/delete/:id', async (req, res) => {
    try {
        await axios.delete(`${API}/events/${req.params.id}`);
    } catch (err) {
        console.error('Delete event error:', err.message);
    }
    res.redirect('/');
});

// ── READ (main page) ─────────────────────────────────────

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
        console.error('Error fetching data:', err.message);
        res.render('index', { members: [], events: [], registrations: [] });
    }
});

// ── REGISTRATIONS ────────────────────────────────────────

// CREATE — checks tier, capacity, and duplicate registration
router.post('/registrations/add', async (req, res) => {
    try {
        const memberId = parseInt(req.body.member_id);
        const eventId  = parseInt(req.body.event_id);

        const [membersRes, eventsRes, regsRes] = await Promise.all([
            axios.get(`${API}/members`),
            axios.get(`${API}/events`),
            axios.get(`${API}/registrations`)
        ]);

        const member = membersRes.data.find(function(m) { return m.id === memberId; });
        const event  = eventsRes.data.find(function(e) { return e.id === eventId; });

        if (!member || !event) {
            console.warn('Member or event not found');
            return res.redirect('/');
        }

        // Tier check: member level must be >= event level
        if (parseInt(member.level) < parseInt(event.level)) {
            console.warn('Tier too low — registration blocked');
            return res.redirect('/?error=tier');
        }

        // Capacity check
        const regCount = regsRes.data.filter(function(r) {
            return r.event_id === eventId;
        }).length;
        if (regCount >= event.capacity) {
            console.warn('Event full — registration blocked');
            return res.redirect('/?error=full');
        }

        // Duplicate registration check
        const alreadyReg = regsRes.data.find(function(r) {
            return r.member_id === memberId && r.event_id === eventId;
        });
        if (alreadyReg) {
            console.warn('Duplicate registration blocked');
            return res.redirect('/?error=duplicate_reg');
        }

        await axios.post(`${API}/registrations`, req.body);
    } catch (err) {
        console.error('Add registration error:', err.message);
    }
    res.redirect('/');
});

// DELETE
router.post('/registrations/delete/:id', async (req, res) => {
    try {
        await axios.delete(`${API}/registrations/${req.params.id}`);
    } catch (err) {
        console.error('Delete registration error:', err.message);
    }
    res.redirect('/');
});

module.exports = router;
