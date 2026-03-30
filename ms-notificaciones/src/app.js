require('dotenv').config();
const express = require('express');
const cors    = require('cors');
const notificacionRoutes = require('./routes/notificacionRoutes');

const app = express();

app.use(cors());
app.use(express.json());

app.use('/api/notificaciones', notificacionRoutes);

app.get('/api/health', (req, res) => {
    res.json({ success: true, service: 'ms-notificaciones', status: 'ok' });
});

module.exports = app;