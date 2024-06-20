import React from 'react';

// Estilos CSS
const styles = `
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  outline: 0;
}

header {
  width: 100%;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

i {
  color: white;
}

.header-icons {
  display: flex;
  gap: 12px;
}

.header-icons a:hover i {
  animation: translateY 0.5s infinite alternate;
  color: rgba(50, 26, 3, 0.782);
}

@keyframes translateY {
  from {
    transform: translateY(0) scale(1);
  }
  to {
    transform: translateY(-8px) scale(1);
  }
}
.header-button {
  border: 1px solid black;
  padding: 8px 24px;
  border-radius: 20px;
  color: black;
  background-color: rgba(247, 245, 245, 0.6352941176);
}

.header-button:hover {
  border: 1px solid rgba(50, 26, 3, 0.782);
  background-color: rgba(50, 26, 3, 0.782);
}

.header-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 15px;
}

@media screen and (max-width: 600px) {
  .header-content {
    width: 100%;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .header-content i {
    margin-top: 16px;
    font-size: 28px;
  }
  .header-logo img {
    width: 160px;
    margin-top: 40px;
  }
  .header-button {
    display: none;
  }
}
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 8px;
}

.bg-home {
  position: relative;
}

.bg-home::before {
  content: "";
  display: block;
  position: absolute;
  background-image: url("imagens/pghome2.png");
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background-size: cover;
  background-repeat: no-repeat;
  background-position: 50% 0;
  opacity: 0.9;
}

.hero {
  color: rgb(9, 9, 9);
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 14px;
}
.hero h1 {
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  text-align: center;
  line-height: 150%;
  max-width: 900px;
  font-size: 30px;
}

.button-contact {
  padding: 14px 28px;
  color: white;
  background-color: red;
  border: 0;
  font-size: 14px;
  font-weight: 400;
  margin: 14px 0;
}

.button-contact:hover {
  animation: scaleButton 0.8s alternate infinite;
}

@keyframes scaleButton {
  from {
    transform: scale(1);
  }
  to {
    transform: scale(1.07);
  }
}
@media screen and (max-width: 770px) {
  .hero {
    min-height: 60vh;
  }
  .hero h1 {
    font-size: 28px;
    padding: 0 14px;
    width: 100%;
  }
}
.about {
  overflow: hidden;
}

.about-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 30px;
  padding: 34px 15px 64px 15px;
}
.about-content img {
  max-width: 1900px;
}

.about-content div {
  flex: 1;
}

.about-discription h2 {
  font-size: 40px;
  margin-bottom: 25px;
}
.about-discription p {
  margin-bottom: 15px;
  line-height: 150%;
}

@media screen and (max-width: 700px) {
  .about-content {
    flex-direction: column;
  }
}
.mobile {
  overflow: hidden;
}

.mobile-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 30px;
  padding: 34px 15px 64px 15px;
}
.mobile-content img {
  max-width: 1900px;
}

@media screen and (max-width: 700px) {
  .mobile-content {
    flex-direction: column;
  }
}
.mobile-conten div {
  flex: 1;
}

.mobile-discription h2 {
  font-size: 40px;
  margin-bottom: 25px;
}
.mobile-discription p {
  margin-bottom: 15px;
  line-height: 150%;
}

.footer {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 55px 0;
  gap: 25px;
  color: white;
  background-color: rgba(255, 68, 0, 0.721);
}

.footer-icons {
  display: flex;
  gap: 8px;
}

body {
  font-family: Arial, Helvetica, sans-serif;
  width: 100%;
  height: 100vh;
  position: relative;
  background-color: rgb(225, 184, 169);
}

button {
  font-family: Arial, Helvetica, sans-serif;
  cursor: pointer;
}

svg {
  width: 100%;
}

img {
  width: 100%;
}
`;

function Inicio() {
    return (
        <div className="bg-home">
            <header>
                <nav className="header-content container">
                    <div className="header-icons">
                        <a href="">
                            <i className="fab fa-instagram fa-2x"></i>
                        </a>
                        <a href="">
                            <i className="fab fa-facebook fa-2x"></i>
                        </a>
                        <a href="">
                            <i className="fab fa-linkedin fa-2x"></i>
                        </a>
                    </div>
                    <div className="header-logo">
                        <img src="../imagens/logo-waitewebnov (2).svg" alt="logo waiter web" />
                    </div>
                    <div>
                        <a className="header-button" href="#"> Entrar em contato </a>
                    </div>
                </nav>
                <main className="hero container">
                    <h1>BEM VINDO AO MELHOR ERP PARA O SEU ESTABELECIMENTO.</h1>
                    <a href="#" className="button-contact" target="_blank"> Entrar em contato </a>
                </main>
            </header>

            <section className="about">
                <div className="container about-content">
                    <div>
                        <img src="../imagens/displaycadast_empre.png" alt="imagem cadastro empresarial" />
                    </div>
                    <div className="about-discription">
                        <h2>UM ERP COMPLETO</h2>
                        <p>Administre o seu estabelecimento por completo através do Waiter Web. Aqui você terá um acompanhamento completo das movimentações do empreendimento, junto como relatórios diários.</p>
                    </div>
                </div>
            </section>

            <section className="mobile">
                <div className="mobile-content">
                    <div>
                        <img src="../imagens/displaycadast_func.png" alt="imagem lista de funcionarios" />
                    </div>
                    <div className="mobile-discription">
                        <h2>MOBILE</h2>
                        <p>Tenha um acompanhamento gerencial em qualquer lugar, além de enviar pedidos à cozinha via celular ou tablet.</p>
                    </div>
                </div>
            </section>

            <footer className="footer">
                <div className="footer-icons">
                    <a href="">
                        <i className="fab fa-instagram fa-2x"></i>
                    </a>
                    <a href="">
                        <i className="fab fa-facebook fa-2x"></i>
                    </a>
                    <a href="">
                        <i className="fab fa-linkedin fa-2x"></i>
                    </a>
                </div>
                <div>
                    <img src="../imagens/logo-waitewebnov (2).svg" alt="logo waiter web" />
                </div>
                <p>Copyright 2024 | Waiter Web - Todos direitos reservados</p>
            </footer>
        </div>
    );
}

export default Inicio;
