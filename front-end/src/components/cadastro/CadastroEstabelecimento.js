import { useState } from 'react'
import styles from '../css/CadastroEstabelecimento.module.css'
import { RiLockPasswordLine, RiLockPasswordFill } from "react-icons/ri";
import { TbNumber } from "react-icons/tb";
import { FaBuilding, FaRegAddressCard, FaRoad } from "react-icons/fa";
import { FaCity, FaTreeCity } from "react-icons/fa6";
import { MdOutlineMail, MdEmail} from "react-icons/md";

function CadastroEstabelecimento(){

    const handleChange = (event) => {
        let { value } = event.target;

        value = value.replace(/\D/g, '');
        value = value.slice(0, 14);

        if (value.length <= 2) {
            value = value.replace(/^(\d{0,2})/, '$1');
          } else if (value.length <= 5) {
            value = value.replace(/^(\d{0,2})(\d{0,3})/, '$1.$2');
          } else if (value.length <= 8) {
            value = value.replace(/^(\d{0,2})(\d{0,3})(\d{0,3})/, '$1.$2.$3');
          } else if (value.length <= 12) {
            value = value.replace(/^(\d{0,2})(\d{0,3})(\d{0,3})(\d{0,4})/, '$1.$2.$3/$4');
          } else {
            value = value.replace(/^(\d{0,2})(\d{0,3})(\d{0,3})(\d{0,4})(\d{0,2})/, '$1.$2.$3/$4-$5');
            
          }
    
        setCNPJ(value);
      };

    function validarEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
      }

    function cadastrar_estabelecimento(e){
      e.preventDefault()

        if (senha !== senha2){
            setMensagem('Senhas não coincidem')
        }
        else{
            setMensagem('')
        }
        if (senha.length < 6){
            setMensagem('Insira uma senha com no minimo 6 caracteres')
        }
        if (email !== confirmarEmail){
            setMensagem('Email não coincidem')
        }
        if (validarEmail(email)) {
            if (cnpj.length === 18){
              const formData = {
                nome,
                cnpj,
                senha,
                cidade,
                bairro,
                rua,
                numero,
                email,
                confirmarEmail
            };
            fetch('/cadastrar', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(formData)
          })
          .then(response => {
            if (response.ok) {
                // Limpar campos e exibir mensagem de sucesso
                setNome('');
                setCNPJ('');
                setCidade('');
                setSenha('');
                setSenha2('');
                setMensagem('Usuário cadastrado com sucesso!');
                setBairro('');
                setRua('');
                setNumero('');
                setEmail('');
                setConfirmarEmail('');
            }
        })
        .catch(error => {
          console.error('Erro ao cadastrar usuário:', error);
          setMensagem('Erro ao cadastrar usuário. Tente novamente.');
      });
            }
            else{
                setMensagem('Insira um CNPJ valido')
            }
          } else {
            setMensagem('Insira um email valido')
          }
        
        
    }

    const [nome, setNome] = useState('');
    const [cnpj, setCNPJ] = useState('');
    const [cidade, setCidade] = useState('');
    const [senha, setSenha] = useState('');
    const [senha2, setSenha2] = useState('');
    const [mensagem, setMensagem] = useState('');
    const [bairro, setBairro] = useState('');
    const [rua, setRua] = useState('');
    const [numero, setNumero] = useState('');
    const [email, setEmail] = useState ('');
    const [confirmarEmail, setConfirmarEmail] = useState ('');

    return(
        <div>
            <form className={styles.form} onSubmit={cadastrar_estabelecimento}>
                <h1>Cadastro Empresarial</h1>
                <div className={styles.inputcontainer}>
                    <div className={styles.inputgroup}>
                        <p className={styles.namegroup}><FaBuilding /> Nome da empresa:</p>
                        <input type="text"
                        className={styles.input} 
                        placeholder="Digite o nome da empresa" 
                        onChange={(e) => setNome(e.target.value)}
                        required/>

                        <p className={styles.namegroup}><FaCity /> Cidade:</p>
                        <input type="text"
                        className={styles.input} 
                        placeholder="Digite a cidade da empresa" 
                        onChange={(e) => setCidade(e.target.value)}
                        required/>

                        <p className={styles.namegroup}><FaRoad /> Rua:</p>
                        <input type="text"
                        className={styles.input} 
                        placeholder="Digite a rua da empresa" 
                        onChange={(e) => setRua(e.target.value)}
                        required/>

                        <p className={styles.namegroup}><MdOutlineMail /> Email:</p>
                        <input type="text"
                        className={styles.input} 
                        placeholder="Digite o email da empresa" 
                        onChange={(e) => setEmail(e.target.value)}
                        required/>
                    
                        <p className={styles.namegroup}><RiLockPasswordLine /> Senha:</p>
                        <input type="password" 
                        className={styles.input}
                        placeholder="Digite sua senha"
                        onChange={(e) => setSenha(e.target.value)} 
                        required/>
                    </div>
                    <div className={styles.inputgroup}>

                        <p className={styles.namegroup}><FaRegAddressCard /> CNPJ:</p>
                        <input type="text" 
                        className={styles.input}
                        placeholder="Digite seu CNPJ"
                        value={cnpj} 
                        onChange={handleChange}
                        required/>

                        <p className={styles.namegroup}><FaTreeCity /> Bairro:</p>
                        <input type="text"
                        className={styles.input} 
                        placeholder="Digite o bairro da empresa" 
                        onChange={(e) => setBairro(e.target.value)}
                        required/>

                        <p className={styles.namegroup}><TbNumber /> Numero:</p>
                        <input type="number"
                        className={styles.input} 
                        placeholder="Digite o numero da empresa" 
                        onChange={(e) => setNumero(e.target.value)}
                        required/>

                        <p className={styles.namegroup}><MdEmail /> Confirme o Email:</p>
                        <input type="text"
                        className={styles.input} 
                        placeholder="Confirme o email da empresa" 
                        onChange={(e) => setConfirmarEmail(e.target.value)}
                        required/>

                        <p className={styles.namegroup}><RiLockPasswordFill /> Confirme sua senha:</p>
                        <input type="password" 
                        className={styles.input}
                        placeholder="Confirme sua senha"
                        onChange={(e) => setSenha2(e.target.value)} 
                        required/>
                    </div>    
                </div>
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

export default CadastroEstabelecimento