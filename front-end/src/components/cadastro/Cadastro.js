import { useState } from 'react'
import styles from '../css/Cadastro.module.css'
import { RiLockPasswordLine, RiLockPasswordFill } from "react-icons/ri";
import { FiUser } from "react-icons/fi";
function Cadastro(){

    function cadastrarUsuario(e){
        if (senha !== senha2){
            setMensagem('Senhas não coincidem')
        }
        else{
            setMensagem('')
        }
        if (senha.length < 6){
            setMensagem('Insira uma senha com no minimo 6 caracteres')
        }
        e.preventDefault()
        console.log('Opção selecionada:', tipoUsuario);
    }
    const trocaUsuario = (opcao) => {
        if (tipoUsuario === opcao) {
          setTipoUsuario(null);
        } else {
          setTipoUsuario(opcao);
        }
      };

    const [tipoUsuario, setTipoUsuario] = useState(null);
    const [nome, setNome] = useState();
    const [usuario, setUsuario] = useState();
    const [senha, setSenha] = useState();
    const [senha2, setSenha2] = useState();
    const [mensagem, setMensagem] = useState('');
    
    return(
        <div>
            <form className={styles.form} onSubmit={cadastrarUsuario}>
                <h1>Cadastro</h1>
                <div className={styles.inputcontainer}>
                    <div className={styles.inputgroup}>
                        <p className={styles.namegroup}><FiUser /> Nome:</p>
                        <input type="text"
                        className={styles.input} 
                        placeholder="Digite seu nome" 
                        onChange={(e) => setNome(e.target.value)}
                        required/>
                        <p className={styles.namegroup}><RiLockPasswordLine /> Senha:</p>
                        <input type="password" 
                        className={styles.input}
                        placeholder="Digite sua senha"
                        onChange={(e) => setSenha(e.target.value)} 
                        required/>
                    </div>
                    <div className={styles.inputgroup}>
                        <p className={styles.namegroup}><FiUser /> Nome de usuario:</p>
                        <input type="text" 
                        className={styles.input}
                        placeholder="Digite seu usuário" 
                        onChange={(e) => setUsuario(e.target.value)}
                        required/>
                        <p className={styles.namegroup}><RiLockPasswordFill /> Confirme sua senha:</p>
                        <input type="password" 
                        className={styles.input}
                        placeholder="Confirme sua senha"
                        onChange={(e) => setSenha2(e.target.value)} 
                        required/>
                    </div>    
                </div>
                <div className="type">
                    <p>Eu sou:</p>
                </div>
                    <label className={styles.labelgroup}>
                        <input
                        className= {styles.checkboxgoup}
                        type= "checkbox"
                        checked={tipoUsuario === 'gerente'}
                        onChange = {(e) => trocaUsuario('gerente')}
                        />
                        Gerente
                    </label>
                    <label className={styles.labelgroup}>
                        <input
                        className= {styles.checkboxgoup}
                        type= "checkbox"
                        checked={tipoUsuario === 'garcom'}
                        onChange = {(e) => trocaUsuario('garcom')}
                        />
                        Garçom
                    </label>
                    <label className={styles.labelgroup}>
                        <input 
                        className= {styles.checkboxgoup}
                        type= "checkbox"
                        checked={tipoUsuario === 'caixa'}
                        onChange = {(e) => trocaUsuario('caixa')}
                        />
                        Caixa
                    </label>
                <div>
                    <p>{mensagem}</p>
                </div>    
                <div>
                    <input className={styles.bottomgroup} type="submit" value="Cadastrar"/>
                </div>
            </form>
        </div>
    )
}

export default Cadastro