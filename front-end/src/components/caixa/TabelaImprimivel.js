import React from 'react';
import styles from '../css/Comandas.module.css';
import { FiPrinter } from "react-icons/fi";

function TabelaImprimivel({ tabelaHtml }) {
  const handleImprimir = () => {
    const janelaPopUp = window.open('', '_blank', 'width=600,height=600');

    janelaPopUp.document.write(`
      <html>
        <head>
          <title>Comanda</title>
          <style>
            @media print {
              @page {
                size: 80mm auto; /* Define o tamanho da página como 80mm de largura e altura automática */
                margin: 0; /* Remove as margens */
              }
              body {
                margin: 0; /* Remove as margens do corpo */
              }
              .tabela-imprimivel, .tabela-imprimivel * {
                visibility: visible;
              }
              .tabela-imprimivel {
                position: absolute;
                left: 0;
                top: 0;
              }
            }
          </style>
        </head>
        <body>
          <div class="tabela-imprimivel">
            ${tabelaHtml}
          </div>
        </body>
      </html>
    `);

    janelaPopUp.document.close();
    janelaPopUp.print();

    setTimeout(() => {
      janelaPopUp.close();
    },); 
  }; 

  return (
    <button className={styles.botaoimprimir} onClick={handleImprimir}><FiPrinter /> Imprimir</button>
  );
}

export default TabelaImprimivel;
