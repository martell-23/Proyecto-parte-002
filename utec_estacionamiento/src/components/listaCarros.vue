<template>
    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <h4 class="card-title">Lista de Carros</h4>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table">
                                <thead class=" text-primary">
                                    <th>
                                        Id
                                    </th>
                                    <th>
                                        Fecha de Ingreso
                                    </th>
                                    <th>
                                        Placa
                                    </th>
                                    <th>
                                        Id de espacio de almacenamiento
                                    </th>
                                    <th>
                                        Opciones
                                    </th>
                                </thead>
                                <tbody>
                                    <tr v-for="carro in carros.carros">
                                        <td>
                                            {{ carro.id }}
                                            <a></a>
                                        </td>
                                        <td>
                                            {{ carro.date }}
                                        </td>
                                        <td>
                                            {{ carro.placa }}
                                        </td>
                                        <td>
                                            {{ carro.id_espacio }}
                                        </td>
                                        <td>
                                            <button class="btn btn-primary" @click="editar(carro)">Facturar</button>
                                            <button class="btn btn-danger" v-on:click='excluir(carro)' >Excluir</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
  name: 'listaCarros',
  data() {
    return {
      carros: [],
      carro: {
        id: '',
        date: '',
        placa: '',
        id_espacio: '',
      },
    };
  },
  methods: {
        editar(carro) {
            
        },
        excluir(carro) {
            this.$http.delete('http://127.0.0.1:5000/carros/' + carro.id).then(response => {
                return response
            });
        },
  },
  created() {
        this.$http.get('http://127.0.0.1:5000/carros', {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
            },
        }
        ).then(res => {
            this.carros = res.body;
            console.log(this.carros);
        });
    },
}
</script>
<style>
.container {
    margin-top: 20px;
    text-align: center;
}
</style>