<template>
    <div>
        <BaseNavbar />
        
        <div class="container">
            <br>
            <h3>Ticket list</h3>
            <br>
            <b-row>
                <b-col>
                    <b-nav-form class="mt-c" style="color">
                        <b-input-group prepend="Sort By">
                            <b-form-select v-model="sortSelected" :options="selectOptions" />
                            <b-form-select v-model="sortOrder" :options="sortOptions" />
                            <b-input-group-append>
                                <b-button  @click="sortOrSearch" variant="info">Sort</b-button>
                            </b-input-group-append>
                        </b-input-group>
                    </b-nav-form>
                </b-col>
                <b-col>
                    <b-nav-form class="float-right">
                        <b-input-group prepend="Filter by">
                            <b-form-select @change="searchChanged" v-model="searchSelected" :options="selectOptions" />
                            <b-form-input v-if="this.searchSelected=='Ticket ID'"  v-model="searchValue" type="text" placeholder="Enter Value"/>
                            <b-form-select v-else v-model="searchValue" :options="valueOptions"/>
                            <b-input-group-append>
                                <b-button  @click="sortOrSearch" variant="info">Search</b-button>
                            </b-input-group-append>
                        </b-input-group>
                    </b-nav-form>
                </b-col>
            </b-row>
            <br>
            <b-row>
                <b-col sm="12">
                    <b-alert fade v-model="showDeletedAlert" variant="success" dismissible>
                            Ticket deleted!
                    </b-alert>
                </b-col>
            </b-row>
            <b-card>
            <b-row>
                <b-col sm="12">
                    
                    <div>
                        <h5 v-if="empty_records" class="text-center">No results matching search criteria.</h5>
                        <b-table v-else borderless striped hover :items="ticket_data" :fields="fields" responsive @row-clicked="getRowData">
                        </b-table>
                    </div>
                    
                </b-col>
            </b-row>
            
            <b-row class="mt-0">
                <b-col sm="12">
                    <b-pagination v-if="!empty_records" :total-rows="number_records" :per-page="limit" @change="changePage" v-model="currentPage" align="right"/>
                </b-col>
            </b-row>
            </b-card>
        </div>
        <div>
            <b-modal ref="row-details-modal" hide-footer title="Ticket details">
                <b-card>
                    <b-container>
                        <b-table borderless small hover :items="selectedTicketData"/>
                    </b-container>
                    <b-button class="mt-3" variant="outline-danger" block @click="deleteRow">Delete Ticket</b-button>
                </b-card>
            </b-modal>
            
        </div>
        <!-- <BaseFooter /> -->
        <br>
    </div>
</template>

<script>
import axios from 'axios';
import BaseNavbar from './BaseNavbar';
// import BaseFooter from './BaseFooter';
import { store } from "./store.js";

export default {
  data() {
    return {
        showDeletedAlert:false,
      ticket_data: [],
      empty_records: false,
      number_records:0,
      currentPage: 1,
      showMessage: false,
      sortSelected: '',
      sortOrder: 1,
      searchValue: '',
      searchSelected: '',
      selectedRowId: '',
      fields: ['Ticket ID', 'Date created', 'Type', 'Priority', 'daysOpen', 'FiledAgainst', 'Severity', 'Satisfaction'],
      limit: 20,
      selectOptions: [
            { value: '', text: 'None' },
            { value: 'Ticket ID', text: 'Ticket ID' },
            { value: 'Type', text: 'Type' },
            { value: 'Severity', text: 'Severity' },
            { value: 'Priority', text: 'Priority' },
            { value: 'daysOpen', text: 'Days Open' },
            { value: 'Satisfaction', text: 'Satisfaction' },
            { value: 'Requestor', text: 'Requestor' },
            { value: 'RequestorSeniority', text: 'Requestor Seniority' },
            { value: 'ITOwner', text: 'IT Owner' },
            { value: 'FiledAgainst', text: 'Filed Against' }
          ],
          sortOptions:[
            { value: '', text: 'Select' },
            { value: '1', text: 'Asc' },
            { value: '-1', text: 'Desc' }
          ],
        valueOptions:[{'value':'', 'text':'Select Value'}],
        selectedTicketData: []
    };
  },
  components: {
    BaseNavbar,
  },
  methods: {
    getData() {
         
      let path =  store.server_url+`/ticketdata?&currentPage=${this.currentPage}&limit=${this.limit}` + 
                `&sortSelected=${this.sortSelected}&sortOrder=${this.sortOrder}` + 
                `&searchSelected=${this.searchSelected}&searchValue=${this.searchValue}`;
      axios.get(path)
        .then((res) => {
          this.ticket_data = res.data.ticket_data;
          this.number_records = res.data.total_items;
          this.empty_records = (this.number_records ? false:true);
          
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    changePage(value) {
        this.currentPage= value;
        this.getData();
    },
    sortOrSearch() {
        this.currentPage = 1;
        this.getData();
    },
    searchChanged() {
        this.searchValue = '';
        if(this.searchSelected == '') {
            this.valueOptions = [{'value':'', 'text':'Select Value'}];
        }
        else {   
            let path =  store.server_url+`/distinct?&field=${this.searchSelected}`;
            axios.get(path)
                .then((res) => {
                this.valueOptions = res.data.value_options;
                })
                .catch((error) => {
                // eslint-disable-next-line
                console.error(error);
                });
        }
    },
    getRowData(data) {
        let selectedTicketData = [];
        var col_list = {'Ticket ID':'Ticket ID',
                    'Type':'Type',
                    'Priority':'Priority',
                    'Date created':'Date created',
                    'daysOpen':'Days Open',
                    'FiledAgainst':'Filed Against',
                    'Severity':'Severity',
                    'Satisfaction':'Satisfaction',
                    'Requestor':'Requestor Employee',
                    'RequestorSeniority':'Requestor Seniority',
                    'ITOwner':'IT Owner'
                    };
        for (var col in col_list){
            selectedTicketData.push({'attribute': col_list[col], 'value':data[col]});
        }
        this.selectedTicketData = selectedTicketData;
        this.$refs['row-details-modal'].show();
        this.selectedRowId = data['_id'];
    },
    deleteRow() {
         
        let path =  store.server_url+`/delete/${this.selectedRowId}`;
        axios.delete(path)
            .then((res) => {
                this.$refs['row-details-modal'].hide();
                this.selectedRowId = '';
                this.getData();
                this.showDeletedAlert = true;
            })
            .catch((error) => {
                // eslint-disable-next-line
                console.error(error);
            });
        
    }
  },
  created() {
    if(store.state.logged_in) {
        this.getData();
    }
    else {
        store.state.unauth_attempt = true;
        this.$router.push('login');
    }
  },
};
</script>

<style>

.page-item.active .page-link{
    /* background-color:#17a2b8;
    border-color:#17a2b8; */
    background-color:#f7c600;
    border-color:#f7c600;
  }

.page-item .page-link{
    color:#f7c600;
  }

.btn-info {
    color: #fff;
    background-color: #f7c600;
    border-color: #ecbe00;
}
.btn-info:hover {
    color: #fff;
    background-color: #e6b901;
    border-color: #e0b400;
}
.btn-info:not(:disabled):not(.disabled):active, .btn-info:not(:disabled):not(.disabled).active, .show > .btn-info.dropdown-toggle {
    color: #fff;
    background-color: #d2a900;
    border-color: #c19c00;
}
.btn-info:focus, .btn-info.focus {
    box-shadow: 0 0 0 0.2rem #ffc10770;
}
.btn-info:not(:disabled):not(.disabled):active:focus, .btn-info:not(:disabled):not(.disabled).active:focus, .show > .btn-info.dropdown-toggle:focus {
    box-shadow: 0 0 0 0.2rem #f5b80194;
}
.page-link:focus {
    z-index: 2;
    outline: 0;
    box-shadow: 0 0 0 0.2rem #ffc10770;
}
</style>