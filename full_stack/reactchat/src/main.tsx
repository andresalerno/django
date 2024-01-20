// Import React for JSX and component creation
import React from 'react';

// Import the ReactDOM library for rendering React components
import ReactDOM from 'react-dom/client';

// Import the main App component from './App.tsx'
import App from './App.tsx';

// Use ReactDOM's createRoot method to create a root in the DOM at the element with id 'root'
ReactDOM.createRoot(document.getElementById('root')!).render(
  // Wrap the entire application in React's StrictMode for additional runtime checks
  <React.StrictMode>
    {/* Render the main App component */}
    <App />
  </React.StrictMode>,
);
