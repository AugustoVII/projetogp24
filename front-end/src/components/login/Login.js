import { useState } from 'react'
import styles from '../css/Login.module.css'
import { RiLockPasswordLine} from "react-icons/ri";
import { FiUser } from "react-icons/fi";
import { FaBuilding } from "react-icons/fa";

function Login(){

    function login(e){
        const formData = {
            username,
            password,
        };
    
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (response.ok) {
                setUsername('');
                setPassword('');
                
            } else {
                setMensagem('Verifique seus dados.');
            }
        })
        .catch(error => {
            console.error('Erro ao logar:', error);
            setMensagem('Verifique seus dados.');
        });
    }

    const trocaUsuario = (opcao) => {
        if (tipoLogin === opcao) {
            setTipoLogin(null);
        } else {
            setTipoLogin(opcao);
        }
      };

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [tipoLogin, setTipoLogin] = useState('Funcionario');
    const [mensagem, setMensagem] = useState('');
    return(
        <div>
            <form className={styles.form} onSubmit={login}>
                <h1>Logar como:</h1>
                    <label className={styles.labelgroup}>
                        <input
                        className= {styles.checkboxgoup}
                        type= "checkbox"
                        checked={tipoLogin === 'Funcionario'}
                        onChange = {(e) => trocaUsuario('Funcionario')}
                        />
                        Funcionario
                    </label>
                    <label className={styles.labelgroup}>
                        <input
                        className= {styles.checkboxgoup}
                        type= "checkbox"
                        checked={tipoLogin === 'Empresa'}
                        onChange = {(e) => trocaUsuario('Empresa')}
                        />
                        Empresa
                    </label>
                    
                <div className={styles.inputcontainer}>
                    <div className={styles.inputgroup}>
                        {tipoLogin === "Funcionario" && 
                        <p className={styles.namegroup}><FiUser /> Login:</p>}
                        {tipoLogin === "Empresa" && <p className={styles.namegroup}><FaBuilding /> CNPJ:</p>}
                        <input type="text"
                        className={styles.input} 
                        placeholder="Digite seus dados"
                        value={username} 
                        onChange={(e) => setUsername(e.target.value)}
                        required/>
                        <p className={styles.namegroup}><RiLockPasswordLine /> Senha:</p>
                        <input type="password" 
                        className={styles.input}
                        placeholder="Digite sua senha"
                        value={password} 
                        onChange={(e) => setPassword(e.target.value)} 
                        required/>
                    </div>
                </div> 
                <div>
                    <p>{mensagem}</p>
                </div>    
                <div>
                    <input className={styles.bottomgroup} type="submit" value="Logar"/>
                </div>
            </form>
        </div>
    )
}

export default Login