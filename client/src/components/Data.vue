<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Data</h1>
        <hr><br><br>
        <br><br>

        <div>
            <b-table striped hover :items="ret_data" :fields="fields">
                <template slot="Actions" slot-scope="row">
                    <b-button size="sm" @click="row.toggleDetails">
                    {{ row.detailsShowing ? 'Hide' : 'Show' }} Details
                    </b-button>
                </template>
            </b-table>
        </div>

      </div>
    </div>

    <!-- <b-modal ref="editDataModal"
             id="data-edit-modal"
             title="Edit"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <td>{{ item.Requestor }}</td>
              <td>{{ item.ITOwner }}</td>
              <td>{{ item.FiledAgainst }}</td>
              <td>{{ item.Severity }}</td>
              <td>{{ item.Priority }}</td>
        <b-form-group id="form-title-edit-group"
                      label="ID:"
                      label-for="form-title-edit-input">
          <b-form-input id="form-id-edit-input"
                        type="text"
                        v-model="editForm._id"
                        required
                        placeholder="Enter ID"
                        disabled>
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-title-edit-group"
                      label="Requestor:"
                      label-for="form-title-edit-input">
          <b-form-input id="form-requestor-edit-input"
                        type="text"
                        v-model="editForm.Requestor"
                        required
                        placeholder="Enter Requestor"
                        disabled>
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-title-edit-group"
                      label="ITOwner:"
                      label-for="form-title-edit-input">
          <b-form-input id="form-itowner-edit-input"
                        type="text"
                        v-model="editForm.ITOwner"
                        required
                        placeholder="Enter ITOwner"
                        disabled>
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-title-edit-group"
                      label="FiledAgainst:"
                      label-for="form-title-edit-input">
          <b-form-input id="form-filedagainst-edit-input"
                        type="text"
                        v-model="editForm.FiledAgainst"
                        required
                        placeholder="Enter FiledAgainst"
                        disabled>
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-title-edit-group"
                      label="Severity:"
                      label-for="form-title-edit-input">
          <b-form-input id="form-severity-edit-input"
                        type="text"
                        v-model="editForm.Severity"
                        required
                        placeholder="Enter Severity"
                        disabled>
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-title-edit-group"
                      label="Priority:"
                      label-for="form-title-edit-input">
          <b-form-input id="form-priority-edit-input"
                        type="text"
                        v-model="editForm.Priority"
                        required
                        placeholder="Enter Priority"
                        disabled>
          </b-form-input>
        </b-form-group>
        
        <b-button type="submit" variant="primary">Update</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal> -->
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert';

export default {
  data() {
    return {
      ret_data: [],
      editForm: {
        _id: '',
        Requestor: '',
        ITOwner: '',
        FiledAgainst: '',
        Severity: [],
        Priority: '',
      },
      message: '',
      showMessage: false,
      // Use these as parameters
      page: 1,
      limit: 10,
      sortSelected: '',
      sortOrder: '', // -1 and 1. Asc and Desc (Write logic for that)
      searchValue: '',
      searchField: '',
      fields: ['Requestor', 'ITOwner', 'FiledAgainst', 'Severity', 'Priority', 'Actions']
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getData() {
      const path = 'http://localhost:5000/data?page=1&limit=10';
      axios.get(path)
        .then((res) => {
          this.ret_data = res.data.ret_data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    updateData(payload, dataID) {
      const path = `http://localhost:5000/data/${dataID}`;
      axios.put(path, payload)
        .then(() => {
          this.getData();
          this.message = 'Data updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getData();
        });
    },
    removeData(dataID) {
      const path = `http://localhost:5000/books/${dataID}`;
      axios.delete(path)
        .then(() => {
          this.getData();
          this.message = 'Data removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getData();
        });
    },
    initForm() {
      this.editForm._id = '';
      this.editForm.Requestor = '';
      this.editForm.ITOwner = '';
      this.editForm.FiledAgainst = '';
      this.editForm.Severity = [];
      this.editForm.Priority = '';
    },
    // onSubmit(evt) {
    //   evt.preventDefault();
    //   this.$refs.addBookModal.hide();
    //   let read = false;
    //   if (this.addBookForm.read[0]) read = true;
    //   const payload = {
    //     title: this.addBookForm.title,
    //     author: this.addBookForm.author,
    //     read, // property shorthand
    //     price: this.addBookForm.price,
    //   };
    //   this.addBook(payload);
    //   this.initForm();
    // },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editDataModal.hide();
      const payload = {
        _id: this.editForm._id,
        Requestor:this.editForm.Requestor,
        ITOwner:this.editForm.ITOwner,
        FiledAgainst:this.editForm.FiledAgainst,
        Severity:this.editForm.Severity,
        Priority:this.editForm.Priority,
      };
      this.updateBook(payload, this.editForm._id);
    },
    // onReset(evt) {
    //   evt.preventDefault();
    //   this.$refs.addBookModal.hide();
    //   this.initForm();
    // },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editDataModal.hide();
      this.initForm();
      this.getData(); // why?
    },
    onDeleteData(item) {
      this.removeData(item._id);
    },
    editData(item) {
      this.editForm = item;
    },
  },
  created() {
    this.getData();
  },
};
</script>
