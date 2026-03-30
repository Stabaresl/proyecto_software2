require('dotenv').config();
const express = require('express');
const cors    = require('cors');

const catalogoRoutes = require('./routes/catalogoRoutes');
const matchingRoutes = require('./routes/matchingRoutes');

const app = express();

app.use(cors());
app.use(express.json());

app.use('/api/catalogo', catalogoRoutes);
app.use('/api/matching', matchingRoutes);

app.get('/api/health', (req, res) => {
    res.json({ success: true, service: 'ms-matching', status: 'ok' });
});

module.exports = app;