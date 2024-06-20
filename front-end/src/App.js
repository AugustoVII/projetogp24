import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import  React  from 'react'
import './App.css';
import CadastroEstabelecimento from './components/cadastro/CadastroEstabelecimento';
import Cadastro from './components/cadastro/Cadastro';
import Login from './components/login/Login';
import listausuarios from './components/listagem/Listagem'
import Navbar from './components/navbar/Navbar'
import Logout from './components/logout/Logout'
import AddProd from './components/gerente/AddProd'
import Mesas from './components/garcom/Mesas'
import Home from './components/home/Inicial'
import Pedidos from './components/cozinheiro/Pedidos'
import PedidosProntos from './components/garcom/Pedidos'
import Inicio from './components/home/Inicio'
import Comandas from './components/caixa/Comandas'

function App() {
  return (
    <div className="App">
      <Router>
      <Navbar />
        <Switch>
        <Route path="/pedidos" component={Pedidos} />
          <Route path="/logout" component={Logout} />
          <Route exact path="/" component={Inicio} />
          <Route path="/cadastrar" component={CadastroEstabelecimento} />
          <Route path="/cadastro" component={Cadastro} />
          <Route path="/login" component={Login} />
          <Route path="/comandas" component={Comandas} />
          <Route path="/listausuarios" component={listausuarios} />
          <Route path="/addproduto" component={AddProd} />
          <Route path='/abrirmesas' component={Mesas} />
          <Route path='/home' component={Home} />
          <Route path='/pedidosprontos' component={PedidosProntos} />
        </Switch>
    </Router>
    </div>
  );
}

export default App;
