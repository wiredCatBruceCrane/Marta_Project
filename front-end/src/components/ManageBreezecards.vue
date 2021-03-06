<template>
  <v-layout column>
    <v-flex xs12 class="text-xs-center" mt-5>
      <h3>Manage Breezecards</h3>
    </v-flex>
    <v-card style="margin-left:20px;margin-right:20px;" flat>
      <v-card-title style="margin-left:20%;margin-right:20%;">
        <v-text-field
          append-icon="search"
          label="Search"
          single-line
          hide-details
          v-model="search"
        ></v-text-field>
      </v-card-title>
      <v-data-table
          v-bind:headers="headers"
          v-bind:items="items"
          v-bind:search="search"
          item-key="card_id"
          class="elevation-1"
        >
        <template slot="items" slot-scope="props">
		      <tr @click="props.expanded = !props.expanded; expand_card(props.item);">
            <td>{{ props.item.card_id }}</td>
            <td class="text-xs-center">${{ props.item.value }}</td>
          </tr>
        </template>
        <template slot="pageText" slot-scope="{ pageStart, pageStop }">
          From {{ pageStart }} to {{ pageStop }}
        </template>
        <template slot="expand" slot-scope="props">
	      <v-card>
	      	<v-card-title>
	          <h3 class="headline mb-0">Manage Card: {{props.item.card_id}}</h3>
	        </v-card-title>
	        <v-card-text>
		          <v-layout row>
	              <v-subheader>Add Value</v-subheader>
	              <v-text-field
	                label="Amount"
	                v-model = "card_update.value"
	                prefix="$"
	              ></v-text-field>
		          </v-layout>
		        </v-card-text>
		        <v-card-actions>
				  <v-flex v-if="!new_card.visible">
				     <v-btn flat color="blue" @click="update_card(props.item, props.expanded)">UPDATE</v-btn>
			   	</v-flex>
			  </v-card-actions>
	      </v-card>
	    </template>
      </v-data-table>
      <v-card-actions>
        <v-flex v-if="!new_card.visible">
            <v-btn flat color="blue" @click.prevent="new_card.visible = true">CREATE CARD</v-btn>
        </v-flex>
      </v-card-actions>
    </v-card>
    <v-card v-if="new_card.visible" style="margin-left: 20px;margin-right: 20px; margin-bottom: 40px; padding: 20px;">
      <v-layout column>
        <h3 class="headline mb-0">Create New Card</h3>
          <v-layout row>
            <v-text-field
              name="card_id"
              label="Card ID"
              id="station_name"
              type="username"
              v-model = "new_card.card_id"
              required>
            </v-text-field>
            <v-flex>
              <v-btn flat color="blue" @click="generate_id">Generate ID</v-btn>
            </v-flex>
          </v-layout>
        </v-layout>
      <v-card-actions>
        <v-flex>
          <v-btn flat color="green" @click="new_card.visible=false;create_new_card()">Create Card</v-btn>
        </v-flex>
        <v-flex class="text-xs-right">
            <v-btn flat @click.prevent="new_card.visible = false" color="red">Cancel</v-btn>
          </v-flex>
      </v-card-actions>
    </v-card>
  </v-layout>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import router from '@/router'
 
Vue.use(VueAxios, axios)

export default {
  props: ['user'],
  data () {
    return {
      max25chars: (v) => v.length <= 25 || 'Input too long!',
      tmp: '',
      search: '',
      pagination: {},
      headers: [
        { text: 'Card ID', value: 'card_id', align: 'left'},
        { text: 'Value', value: 'value', align: 'center'}
      ],
      items: [],
      card_update: {
      	card_id: '',
      	value: 0,
      	owner: ''
      },
      new_card: {
        visible: false,
        card_id: '',
        owner: this.user.auth.username,
        value: 0
      },
      rules: {
        required: (value) => !!value || 'Required.',
        email: (value) => {
          const pattern = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          return pattern.test(value) || 'Invalid e-mail.'
        },
        breezecard: (value) => {
          const pattern = /\d{16}/g
          return pattern.test(value) || 'Invalid breezecard.'
        },
        notempty: (value) => {
          /^$|\s+/
          const pattern = /^$|\s+/
          return pattern.test(value) || 'Cannot be empty.'
        }
      }
    }
  },
  methods: {
  	refresh_breezecards() {
    	//now this is going to be run when they mount.
	    var url = "http://54.173.144.94:5000/get_user_breezecards"
      var body = {
        "owner":this.user.auth.username
      }
	    axios.post(url, body)
	        .then((response) => {
	          this.items = response.data
	        })
	        .catch(error => {
	          alert('Hmmm something went wrong with our servers when fetching stations!! Sorry!')
	    });
    },
    update_card(item, expanded) {
    	//now this is going to be run when they mount.
	    var url = "http://54.173.144.94:5000/update_card"
    	this.card_update.owner = item.owner
      this.card_update.card_id = item.card_id
      if (!Number.isInteger(this.card_update.value) || parseInt(this.card_update.value) < 0 || parseInt(this.card_update.value) > 1000) {
        alert('not a valid input')
        return
      }
      this.card_update.value = parseInt(this.card_update.value)
    	this.card_update.value += parseInt(item.value)
	    axios.post(url, this.card_update)
	        .then((response) => {
	          this.refresh_breezecards()
	          this.card_update.value = 0
            expanded = false; 
	        })
	        .catch(error => {
	          alert('Hmmm something went wrong with our servers when fetching stations!! Sorry!')
	    });
    },
    create_new_card() {
      var url = "http://54.173.144.94:5000/add_new_card"

      if (this.new_card.card_id < 0) {
        alert('bad card value!')
      }

      const pattern = /\d{16}/
      if (!pattern.test(this.new_card.card_id)) {
        alert('bad breezecard id!')
        return
      }

      axios.post(url, this.new_card)
          .then((response) => {
            this.refresh_breezecards()
          })
          .catch(error => {
            alert('Hmmm something went wrong with our servers when fetching stations!! Sorry!')
      });
    },
    generate_id() {

      this.new_card.card_id = (Math.random()+' ').substring(2,10)+(Math.random()+' ').substring(2,10);
    }
  },
  beforeMount() {
  	this.refresh_breezecards()
  },
  mounted() {
    this.refresh_breezecards()
  }
}
</script>