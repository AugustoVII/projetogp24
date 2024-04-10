import  React  from 'react'
import './App.css';
import CadastroEstabelecimento from './components/cadastro/CadastroEstabelecimento';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Login from './components/login/Login';
function App() {
  return (
    <div className="App">
      <Router>
      <div>
        <Switch>
          <Route exact path="/" component={CadastroEstabelecimento} />
          <Route path="/cadastrar" component={CadastroEstabelecimento} />
          <Route path="/login" component={Login} />
        </Switch>
      </div>
    </Router>
    </div>
  );
}

export default App;
