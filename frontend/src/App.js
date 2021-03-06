import React from 'react';
import './App.css';
import Home from './home'
import Login from './login'
import Signup from './signup'
import {Switch, Route, Redirect, BrowserRouter} from 'react-router-dom'
import Footer from './footer';
import SignupOnBoard from './signupOnboard'

function App() {
  return (
    <div>
      
      <BrowserRouter>
      <Switch>
        <Route path='/home' component={() => <Home />} />
        <Route exact path='/login' component={() => <Login />} />
        <Route exact path='/signup' component={() => <Signup />} />
        <Route exact path='/api/verify/:uid/:token' component={SignupOnBoard} />
        <Redirect to='/home' />
      </Switch>
      </BrowserRouter>
      <Footer />
    </div>
  );
}

export default App;