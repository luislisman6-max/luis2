import { saludo } from './saludo';

const app = document.querySelector<HTMLDivElement>('#app')!;
app.innerHTML = `<h1>${saludo('')}</h1>`;
