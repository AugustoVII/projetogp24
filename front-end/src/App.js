import  React  from 'react'
import './App.css';
import CadastroEstabelecimento from './components/cadastro/CadastroEstabelecimento';
import Cadastro from './components/cadastro/Cadastro';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Login from './components/login/Login';
import listausuarios from './components/listagem/Listagem'
import Navbar from './components/navbar/Navbar'
import Logout from './components/logout/Logout'

function App() {
  return (
    <div className="App">
      <Router>
      <Navbar />
        <Switch>
          <Route path="/logout" component={Logout} />
          <Route exact path="/" component={CadastroEstabelecimento} />
          <Route path="/cadastrar" component={CadastroEstabelecimento} />
          <Route path="/cadastro" component={Cadastro} />
          <Route path="/login" component={Login} />
          <Route path="/listausuarios" component={listausuarios} />
        </Switch>
    </Router>
    </div>
  );
}

export default App;
