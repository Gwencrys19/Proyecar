document.addEventListener("DOMContentLoaded", function() {
  cargarDatosGuardados()
  calcular()
    
  function cargarDatosGuardados() {
    const data = JSON.parse(localStorage.getItem('dataTableData')) || [];
    const table = document.getElementById('transactionTable').getElementsByTagName('tbody')[0];
    data.forEach(item => {
      const newRow = table.insertRow();
      const cell1 = newRow.insertCell(0);
      const cell2 = newRow.insertCell(1);
      const cell3 = newRow.insertCell(2);
      const cell4 = newRow.insertCell(3);
      const cell5 = newRow.insertCell(4);
      
      cell1.textContent = item.nombre;
      cell2.textContent = item.precio;
      cell3.textContent = item.cantidad;
      cell4.textContent = item.valor;
      cell5.innerHTML = '<td><button id="borrar">borrar</button></td>'
     
    });
  }
 const forms = Array.from(document.querySelectorAll('#formulario'));
 
  forms.forEach(form=>{
  form.addEventListener("submit",function(event){
   
    let formData=new FormData(form);
    insertRowinTable(formData)
  })
function insertRowinTable(formDatas){
  let TableRef = document.getElementById("transactionTable");
  
  let newRowRef = TableRef.insertRow(TableRef.rows.length - 1);
  
  let newTypeCellRef = newRowRef.insertCell(0);
  const nombre = formDatas.get("nombre");
  newTypeCellRef.textContent = nombre

  newTypeCellRef = newRowRef.insertCell(1);
  const precio = formDatas.get("precio"); 
  newTypeCellRef.textContent = precio;

  newTypeCellRef = newRowRef.insertCell(2);
  const cantidad = formDatas.get("cantidad"); 
  newTypeCellRef.textContent = cantidad;

  newTypeCellRef = newRowRef.insertCell(3);
  const valor = parseInt(cantidad * precio);
  newTypeCellRef.textContent = valor;
  
  
  const data = JSON.parse(localStorage.getItem('dataTableData')) || [];
  data.push({ nombre, precio, cantidad ,valor});
  localStorage.setItem('dataTableData', JSON.stringify(data)); 

}
// Guardar los datos en localStorage
const reset =document.getElementById("reset");
reset.addEventListener("click",function(event){
  event.preventDefault();
  localStorage.clear();
  window.location.href="/carrito/"; 
}); 
});

function calcular(){

var filas=document.querySelectorAll("#transactionTable tbody tr");

var total=0

filas.forEach(function(e){
  var columnas=e.querySelectorAll("td");

  var cantidad=parseFloat(columnas[1].textContent);
  var importe=parseFloat(columnas[2].textContent);


  total+=cantidad*importe;
  localStorage.setItem('total',total);
});
 
var tabla = document.getElementById("transactionTable");
const GLOBAL_CONSTANT =total
var ultimaFila = tabla.rows[tabla.rows.length - 1];  
var ultimaColumna = ultimaFila.cells[ultimaFila.cells.length - 1];
var filas=document.querySelectorAll("#transactionTable tfoot tr td");

filas[1].textContent=localStorage.getItem('total');

}

const borrar=Array.from(document.querySelectorAll('#borrar'));
// Obtener los datos almacenados en localStorage bajo la clave 'dataTableData'
var dataTableData = JSON.parse(localStorage.getItem('dataTableData'));
borrar.forEach(boton=>{
  boton.addEventListener("click",
function (fila) {
  
  var fila = boton.parentNode.parentNode;// Obtener la fila actual
  var rowIndex = fila.rowIndex;// Obtener el índice de la fila en la tabla
  // Eliminar la fila de la tabla
  fila.parentNode.removeChild(fila);
  // Eliminar el elemento correspondiente de 'dataTableData'
  dataTableData.splice(rowIndex - 1, 1);

  // Guardar los datos actualizados en localStorage
  localStorage.setItem('dataTableData', JSON.stringify(dataTableData));
  
  // calcular los valores nuevamente
  calcular()
   

})});


});