```javascript
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('Hello from blog-app');
});

app.post('/login', (req, res) => {
  // Here you would handle the login logic
  res.send('Login route');
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```