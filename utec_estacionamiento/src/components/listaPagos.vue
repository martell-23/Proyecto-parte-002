<template>
    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <h4 class="card-title">Lista de Pagos</h4>
                    </div>
                    <div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <div class="table">
                                    <thead class=" text-primary">
                                        <th>
                                            Id
                                        </th>
                                        <th>
                                            Placa
                                        </th>
                                        <th>
                                            Monto
                                        </th>
                                    </thead>
                                    <tbody>
                                        <tr v-for="pago in pagos.pagos" :key="pago.id">
                                            <td>
                                                {{ pago.id }}
                                            </td>
                                            <td>
                                                {{ pago.placa }}
                                            </td>
                                            <td>
                                                {{ pago.monto }}
                                            </td>
                                        </tr>
                                    </tbody>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'listaPagos',
  data () {
    return {
      pagos: [],
      pago: {
        id: '',
        placa: '',
        monto: ''
      }
    }
  },
  methods: {
        
  },
  created() {
        this.$http.get('http://127.0.0.1:5000/pagos', {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
            },
        }
        ).then(res => {
            this.pagos = res.body;
            console.log(this.pagos);
        });
    },
}
</script>
