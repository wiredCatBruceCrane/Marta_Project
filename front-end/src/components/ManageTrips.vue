<template>
  <v-layout column>
    <v-flex xs12 class="text-xs-center" mt-5>
      <h3>Manage Trips</h3>
    </v-flex>
    <v-card style="margin: 20px; padding: 5px;">
      <v-layout column>
	  	<v-flex xs11 sm5>
		  	<v-select
		        :items="breezecards"
		        item-text="card_id"
		        item-value=""
		        v-model="breezecard_select"
		        label="Select Breezecard"
		        single-line
		        @input="get_current_trip()"
		        bottom
	        ></v-select>
	    </v-flex>
	    <h4 class="headline mb-0">Balance: ${{breezecard_select.value}}</h4>
	    <v-layout row>
		  	<v-flex xs11 sm5>
		        <v-select
			        :items="stations"
			        item-text="station_name"
			        v-model="station_start_select"
			        label="Start Station"
			        :disabled="current_trip.live"
			        single-line
			        bottom
		        ></v-select>
		    </v-flex>
			<v-card-actions class="text-xs-left">
				<v-flex>
				    <v-btn primary flat type="submit" v-on:click="start_trip()">Start Trip</v-btn>
				  </v-flex>
			</v-card-actions>
	    	<h4 v-if="current_trip.live" class="headline mb-0">Trip in Progress: {{this.current_trip.station_name}}</h4>
	    	<v-spacer/>
	    	<h4 v-if="current_trip.live" class="headline mb-0">Trip Fare: {{this.current_trip.tripfare}}</h4>
	    	<h4 v-if="!current_trip.live" class="headline mb-0">No Current Trip</h4>
		</v-layout>
		<v-layout>
		    <v-flex xs11 sm5>
		        <v-select
			        :items="end_stations"
			        item-text="station_name"
			        v-model="station_end_select"
			        label="End Station"
			        :disabled="!current_trip.live"
			        single-line
			        bottom
		        ></v-select>
		    </v-flex>
		    <v-card-actions class="text-xs-left">
		        <v-flex>
		            <v-btn primary flat type="submit" v-on:click="end_trip()">End Trip</v-btn>
		          </v-flex>
		    </v-card-actions>
		</v-layout>
	  </v-layout>
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
	      stations: [],
	      end_stations: [],
	      breezecard_select: {
	      	value: '',
	      	card_id: 0
	      },
	      station_start_select: null,
	      station_end_select: null,
	      breezecards: [],
	      start_picker: {
	        date: '2017-10-1',
	        menu: false
	      },
	      end_picker: {
	        date: '2017-12-25',
	        menu: false 
	      },
	      current_trip: {
	      	live: false,
	      	tripfare: 0,
	      	station_name: ''
	      }
	    }
	},
	methods: {
    	refresh_stations() {
	  		//now this is going to be run when they mount.
	    	var url = "http://54.173.144.94:5000/get_stations"

	    	axios.get(url)
		        .then((response) => {
		          var stations = response.data
		          this.stations = stations
		          this.end_stations = stations
		        })
		        .catch(error => {
		          alert('Hmmm something went wrong with our servers when fetching stations!! Sorry!')
		      });
  		},
  		refresh_breezecards() {
	    	//now this is going to be run when they mount.
		    var url = "http://54.173.144.94:5000/get_user_breezecards"
		    if (this.user == null) {
		    	this.$emit('logout')
		    	this.$emit('goHome')
		    }
	        var body = {
	           "owner":this.user.auth.username
	        }
		    axios.post(url, body)
		        .then((response) => {
		          this.breezecards = response.data
		        })
		        .catch(error => {
		          alert('Hmmm something went wrong with our servers when fetching stations!! Sorry!')
		    });
	    },
	    start_trip() {

	    	var url = "http://54.173.144.94:5000/start_trip"

	    	var body = {
				"stopid": this.station_start_select.stop_id,
				"card_id": this.breezecard_select.card_id,
				"trip_fare": this.station_start_select.fare
			}

	    	axios.post(url, body)
		        .then((response) => {
	    	      this.current_trip.live = true
	    	      this.current_trip.tripfare = this.station_start_select.fare
		        })
		        .catch(error => {
		          alert('Hmmm something went wrong with our servers when fetching stations!! Sorry!')
		      });
	    },
	    end_trip() {

			var url = "http://54.173.144.94:5000/end_trip"

			var body = {
				"endstopid": this.station_end_select.stop_id,
				"card_id": this.breezecard_select.card_id
			}

			axios.post(url, body)
		        .then((response) => {
		          var stations = response.data
				  this.current_trip.tripfare = 0
		          this.current_trip.live = false
		          this.current_trip.station_name = ''
		        })
		        .catch(error => {
		          alert('Hmmm something went wrong with our servers when fetching stations!! Sorry!')
		      });
	    }, 
	    get_current_trip() {
			var url = "http://54.173.144.94:5000/get_current_trip"

			var body = {
				"card_id": this.breezecard_select.card_id
			}

			axios.post(url, body)
		        .then((response) => {
		          var station = response.data.station
		          var tripfare = response.data.tripfare
		          if (station == null) {
		          	this.current_trip.live = false
		          } else {
		            this.current_trip.tripfare = tripfare
		            this.current_trip.live = true
		            this.current_trip.station_name = station.station_name
		          }
		        })
		        .catch(error => {
		          alert('Hmmm something went wrong with our servers when fetching stations!! Sorry!')
		      });
	    }
	},
    beforeMount(){
    	this.refresh_stations()
    	this.refresh_breezecards()
    }
}
</script>