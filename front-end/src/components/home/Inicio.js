// Pedidos.js
import React, { useState, useEffect } from 'react';
import styles from '../css/Inicio.module.css';
import displaycadast_func from '../imagens/displaycadast_func.png';
import logowaitewebnov from '../imagens/logo-waitewebnov (2).svg';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faInstagram, faFacebook, faLinkedin } from '@fortawesome/free-brands-svg-icons';
import { useHistory } from 'react-router-dom';

function Inicio() {
    const history = useHistory();
    const handleSubitemClick = (rota) => {
        history.push(rota);
      };

  return (
   <div>
        <div className={styles.bghome}>
        <header>
            <nav className={styles.headercontent}>
            
                <div className={styles.headerlogo}>
                    <img className={styles.img} src={logowaitewebnov} alt="logo waiter web"/>

                </div>
                 <div className={styles.botao}>

                 <a className={styles.headerbutton} href="#"> Entrar em contato</a>        
                 </div>
            </nav>
            <main class="hero container">
            <h1>BEM VINDO AO MELHOR ERP PARA O SEU ESTABELECIMENTO. </h1>
            <div className={styles.botoes}>
              <a className={styles.headerbutton} onClick={() => handleSubitemClick('/login')}> Login</a> 
              <a className={styles.headerbutton} onClick={() => handleSubitemClick('/cadastrar')}> Cadastro</a> 
            </div>
            </main>
        
        </header>

    </div>

     
    <section className={styles.about}>
        <div className={styles.aboutcontent}>
            <div>
                <img className={styles.img} src={displaycadast_func} alt="imagem cadastro empresarial"/>
            </div>
                
                <div className={styles.aboutdiscription}>
                    <h2>UM ERP COMPLETO</h2>
                  <p>Administre o seu estabelecimento por completo através do Waiter Web. Aqui você terá um acompanhamento completo das movimentações do empreendimento, junto como relatórios diários.</p>
                </div>
            </div>

    </section>
<section className={styles.mobile}>
        <div className={styles.mobilecontent}>
            <div>
                <img className={styles.img} src={displaycadast_func} alt="imagem cadastro empresarial"/>
            </div>
                
                <div className={styles.mobilediscription}>
                    <h2>MOBILE</h2>
                  <p>Tenha um acompanhamento gerencial em qualquer lugar, alem de enviar pedidos a cozinha via celular ou tablet.</p>
                </div>
            </div>
    </section>

    <footer className={styles.footer}>
        <div className={styles.icons}>
            <a href="">
                <i class="fa-brands fa-instagram fa-2x"></i>
            </a>
            <a href="">
                <i class="fa-brands fa-facebook fa-2x"></i>
            </a>
            <a href="">
                <i class="fa-brands fa-linkedin fa-2x"></i>
            </a>
        </div>

        <div>
            <img className={styles.img} src={logowaitewebnov} alt="logo waiter web"/>
            <div className={styles.headericons}>
              <a href="#">
                <FontAwesomeIcon icon={faInstagram} size="2x" color="white" />
              </a>
              <a href="#">
                  <FontAwesomeIcon icon={faFacebook} size="2x" color="white"/>
              </a>
              <a href="#">
                  <FontAwesomeIcon icon={faLinkedin} size="2x" color="white"/>
              </a>
          </div>
        </div>
        <p>Copyright 2024 | Waiter Web - Todos direitos reservados</p>
    </footer>
   </div>
  );
}

export default Inicio;
