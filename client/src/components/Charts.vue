<template>
    <div>
      <BaseNavbar />
      <div class="container">
          <br>
          <b-row>
          <h3>Analytics report</h3>
          </b-row>
          <br>
          <b-card>
            <div class="container">

              <h4>General information</h4>
            <b-row>
              <b-col>
                This is some description of the graph on the left.
                <b-button disabled variant="warning">Warning</b-button>
                <div>
                  <b-alert show variant="success">
                    <h4 class="alert-heading">Well done!</h4>
                    <p>
                      Aww yeah, you successfully read this important alert message. This example text is going to
                      run a bit longer so that you can see how spacing within an alert works with this kind of
                      content.
                    </p>
                    <hr>
                    <p class="mb-0">
                      Whenever you need to, be sure to use margin utilities to keep things nice and tidy.
                    </p>
                  </b-alert>
                </div>
              </b-col>
              <b-col sm="6" lg="4" offset-lg="1" offset-sm="3">
                <PieChart :field=field3></PieChart>
              </b-col> 
            </b-row>
            <br><br>

              <h4>Satisfaction</h4>
            <b-row>
              <b-col sm="6" lg="4" offset-lg="1" offset-sm="3">
                <BarChart :field=field2></BarChart>
                
              </b-col>
              <b-col >
                This is some description of the graph on the left.
                <b-button disabled variant="warning">Warning</b-button>
                <div>
                  <b-alert show variant="success">
                    <h4 class="alert-heading">Well done!</h4>
                    <p>
                      Aww yeah, you successfully read this important alert message. This example text is going to
                      run a bit longer so that you can see how spacing within an alert works with this kind of
                      content.
                    </p>
                    <hr>
                    <p class="mb-0">
                      Whenever you need to, be sure to use margin utilities to keep things nice and tidy.
                    </p>
                  </b-alert>
                </div>
              </b-col> 
            </b-row>


              <h4>Priority</h4>
            <b-row>
              <b-col>
                This is some description of the graph on the left.
                <b-button disabled variant="warning">Warning</b-button>
                <div>
                  <b-alert show variant="success">
                    <h4 class="alert-heading">Well done!</h4>
                    <p>
                      Aww yeah, you successfully read this important alert message. This example text is going to
                      run a bit longer so that you can see how spacing within an alert works with this kind of
                      content.
                    </p>
                    <hr>
                    <p class="mb-0">
                      Whenever you need to, be sure to use margin utilities to keep things nice and tidy.
                    </p>
                  </b-alert>
                </div>
              </b-col>
              <b-col sm="6" lg="4" offset-lg="1" offset-sm="3">
                <PieChart :field=field1></PieChart>
              </b-col> 
            </b-row>
            <br><br>
            
            <h4>Days open</h4>
            <br>
            <b-row>
              <b-col lg="12">
              <LineChart :field=field></LineChart>
              </b-col>
            </b-row>

            <br>
            <h4>Additional</h4>
            <br>
            <b-row>
              <b-col>
                <p> In the data, Requests have higher priorities than issues.
                <p> There is one record that has no date (TicketID: 15865) </p>
              </b-col>
              <b-col  sm="6" lg="4" offset-lg="1" offset-sm="3">
                <BarChartDual :field=field1 :cat_by=cat_by></BarChartDual>
              </b-col>  
            </b-row>
            </div>
          </b-card>
      </div>
      <br>
      <!-- <BaseFooter /> -->
    </div>
</template>

<script>
import axios from 'axios';
import { store } from "./store.js";
import BaseNavbar from './BaseNavbar';
import LineChart from './BaseLinechart';
import BarChart from './BaseBarchart';
import PieChart from './BasePiechart';
import BarChartDual from './BaseBarChartDual';
// import BaseFooter from './BaseFooter';

export default {
  data() {
    return {
      field1: "Priority",
      field2: "Satisfaction",
      field3: "Type",
      cat_by: "Type",
      };
  },
  components: {
    BaseNavbar,
    LineChart,
    BarChart,
    PieChart,
    BarChartDual,
  },
  methods: {
  },
  created() {

    if(store.state.logged_in) {
    }
    else {
        store.state.logout_init = false;
        store.state.unauth_attempt = true;
        store.state.attempt_path = this.$route.path;
        this.$router.push('login');
    }
  },
};
</script>
