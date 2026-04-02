
const express = require('express');
const router = express.Router();
const { check, validationResult } = require('express-validator');

// Mock user database (for demonstration purposes)
const users = [
    { username: 'user1', password: 'password1' },
    { username: 'user2', password: 'password2' }
];

// Login route
router.post('/login', [
    check('username').isLength({ min: 1 }).withMessage('Username is required'),
    check('password').isLength({ min: 1 }).withMessage('Password is required')
], (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
    }

    const { username, password } = req.body;
    const user = users.find(user => user.username === username && user.password === password);

    if (user) {
        // Ideally, create and return a JWT or session here
        return res.status(200).json({ message: 'Login successful', user });
    } else {
        return res.status(401).json({ message: 'Invalid credentials' });
    }
});

module.exports = router;