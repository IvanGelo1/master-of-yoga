import './App.css';
import { ReactElement } from 'react';
import { Switch, Route } from 'react-router-dom';

import About from './pages/About';
import UserAuth from './pages/UserAuth';
import LandingPage from './pages/LandingPage';
import PageNotFound from './pages/PageNotFound';

function App(): ReactElement {
  return (
    <div className="App">
      <Switch>
        <Route path="/" component={LandingPage} exact />
        <Route path="/about" component={About} />
        <Route path="/enter" component={UserAuth} />
        <Route component={PageNotFound} />
      </Switch>
    </div>
  );
}

export default App;