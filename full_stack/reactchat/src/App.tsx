// Import the 'Home' component from the "./pages" directory
import Home from "./pages/Home";

// Import necessary components and functions from the 'react-router-dom' library
import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from "react-router-dom";

// Create a router using 'createBrowserRouter' and define routes using 'createRoutesFromElements'
const router = createBrowserRouter(
  createRoutesFromElements(
    // Define a single route for the path "/" that renders the 'Home' component
    <Route>
      <Route path="/" element={<Home />} />
    </Route>
  )
);

// Define the main 'App' component
const App = () => {
  // Return the 'RouterProvider' component, providing the 'router' object as a prop
  return <RouterProvider router={router} />;
};

// Export the 'App' component as the default export of this module
export default App;
