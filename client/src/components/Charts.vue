<template>
  <div>
    <BaseNavbar/>
    <div class="container">
      <br>
      <b-row>
        <h3>Analytics report</h3>
      </b-row>
      <br>
      <b-card>
        <div class="container">
          
          <b-row>
            <b-col>
              <br>
              <h4>General information</h4>
              <br>
              There are a total of 25628 records.
              <br>
              <div>
                <br>
                <b-alert show variant="success">
                  <p
                    class="mb-0"
                  >A majority of the tickets are of type Request (74%).</p>
                </b-alert>
                <p>The numbers and plot points can be seen by hovering over the graph</p>
                <p>Tickets can be viewed grouped by this or any other attribute in the Tickets tab</p>
              </div>
            </b-col>
            <b-col sm="6" lg="4" offset-lg="1" offset-sm="3">
              <PieChart :field="field3"></PieChart>
            </b-col>
          </b-row>
          <br>
          <br>

          <h4>Satisfaction</h4>
          <b-row>
            <b-col sm="6" lg="4" offset-lg="1" offset-sm="3">
              <BarChart :field="field2"></BarChart>
            </b-col>
            <b-col>
              The graph on the left shows the tickets grouped by Satisfaction. <br>
              <div>
                <br>
                <b-alert show variant="warning">
                  <p class="mb-0">
                    A majority of the tickets are of unknown satisfaction (31%)
                  </p>
                </b-alert>
                <p>Aside from those unknown, over 41% of the remaining tickets are highly satisfied. (28% of the whole data) </p>
              </div>
            </b-col>
          </b-row>

          
          <b-row>
            <b-col>
              <br><br>
              <h4>Priority</h4>
              <br>
              The plot of the right shows fractions of tickets grouped by priority.
              <div> <br>
                <b-alert show variant="danger">
                  <p
                    class="mb-0"
                  >Over 30% of the tickets have not been assigned priority.</p>
                </b-alert>
                <br> <p> Of the remaining, a majority (51%) of the tickets are of high priority. (36% of the whole data)</p>
              </div>
            </b-col>
            <b-col sm="6" lg="4" offset-lg="1" offset-sm="3">
              <PieChart :field="field1"></PieChart>
            </b-col>
          </b-row>
          <br>
          <br>

          <h4>Days open</h4>
          <br>
          <b-row>
            <b-col lg="12">
              <LineChart :field="field"></LineChart>
            </b-col>
            <b-col>
              <p> The above plot shows the number of tickets grouped by the Days Open attribute.</p>
              <p> 47% of the tickets have been open for over 5 days. The rest (53%) are between 0 and 5 days.</p>
              <b-alert show variant="secondary">
                  <p
                    class="mb-0"
                  >24% of the tickets have been open for zero days.</p>
                </b-alert>
            </b-col>
          </b-row>

          <br>
          
          <br>
          <b-row>
            <b-col>
              <h4>Additional</h4>
              <br>
              <p>The graph on the right shows the priorities of tickets grouped by Ticket type.</p>
              <br>
              <b-alert show variant="info">
                  <p
                    class="mb-0"
                  >There is one ticket that has no date (TicketID: 15865).</p>
                </b-alert>
            </b-col>
            <b-col sm="6" lg="4" offset-lg="1" offset-sm="3">
              <BarChartDual :field="field1" :cat_by="cat_by"></BarChartDual>
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
import axios from "axios";
import { store } from "./store.js";
import BaseNavbar from "./BaseNavbar";
import LineChart from "./BaseLinechart";
import BarChart from "./BaseBarchart";
import PieChart from "./BasePiechart";
import BarChartDual from "./BaseBarChartDual";
// import BaseFooter from './BaseFooter';

export default {
  data() {
    return {
      field1: "Priority",
      field2: "Satisfaction",
      field3: "Type",
      cat_by: "Type"
    };
  },
  components: {
    BaseNavbar,
    LineChart,
    BarChart,
    PieChart,
    BarChartDual
  },
  methods: {},
  created() {
    if (store.state.logged_in) {
    } else {
      store.state.logout_init = false;
      store.state.unauth_attempt = true;
      store.state.attempt_path = this.$route.path;
      this.$router.push("login");
    }
  }
};
</script>
