<template>
  <v-app>
    <v-navigation-drawer temporary v-model="sidebar">
      <v-list>
        <v-list-tile
          v-for="item in toolbar"
          :key="item.title"
          :to="item.path"
          :color="item.color">
          <v-list-tile-content>{{ item.title }}</v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>

    <v-toolbar fixed flat color="white">
      <span class="hidden-sm-and-up">
        <v-toolbar-side-icon @click.stop="sidebar = !sidebar">
        </v-toolbar-side-icon>
      </span>
      <v-toolbar-title>
        <router-link :to="home" tag="span" style="cursor: pointer">
          <v-icon large>
            business
          </v-icon>
          <!-- {{ appTitle }} -->
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-xs-only">
        <v-btn
          flat
          v-for="item in toolbar"
          :key="item.title"
          :color="item.color"
          :to="item.path">
          {{ item.title }}
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>
    
    <main style="background-color:white; margin-top: 30px;">
      <v-container pa-0 fluid>
        <router-view :user='userinfo' v-on:setPassengerToolbar = "setPassengerToolbar" v-on:logout="logout" v-on:setAdminToolbar = "setAdminToolbar" v-on:home="goHome" v-on:login="login"></router-view>
      </v-container>
    </main>
    
  </v-app>
</template>

<script>
  import router from '@/router'

  export default {
    data () {
      return {
        userinfo: null,
        appTitle: 'HSK',
        home: "/",
        sidebar: false,
        standardToolbar: [
          { title: 'Login', path: '/signin', icon: 'face', color: "blue"},
          { title: 'Register', path: '/signup', icon: 'lock_open', color: "green"}
        ],
        passengerToolbar: [
          { title: 'Breezecards', path: '/manageuserbreezecards', icon: 'home', color: "grey"},
          { title: 'Trips', path: '/managetrips', icon: 'home', color: "grey"},
          { title: 'Trip History', path: '/triphistory', icon: 'lock_close', color: "grey"},
          { title: 'Logout', path: '/logout', icon: 'lock_close', color: "red" }
        ],
        adminToolbar: [
          { title: 'Stations', path: '/stationmanagement', icon: 'face', color: "grey"},
          { title: 'Susp. Cards', path: '/suspendedcards', icon: 'face', color: "grey"},
          { title: 'Breezecards', path: '/breezecardmanagement', icon: 'face', color: "grey"},
          { title: 'Pass. Flow', path: '/passengerflowreport', icon: 'face', color: "grey"},
          { title: 'Logout', path: '/logout', icon: 'lock_close', color: "red" }
        ],
        toolbar: [
          { title: 'Career', path: '/career', icon: 'home', color: "grey"},
          { title: 'Company', path: '/company', icon: 'face', color: "grey" },
          { title: 'Login', path: '/signin', icon: 'face', color: "blue"},
          { title: 'Register', path: '/signup', icon: 'lock_open', color: "green"}
        ]
      }
    },
    methods: {
      login(userinfo){
        this.userinfo = userinfo
        this.load_bar()
        this.goHome()
      },
      load_bar(){
        if (this.userinfo == null) {
          this.setStandardToolbar()
        } else if (this.userinfo.isadmin) {
          this.setAdminToolbar()
        } else {
          this.setPassengerToolbar()
        }
      },
      setPassengerToolbar() {
        this.toolbar = this.passengerToolbar
        this.home = "/passengerdashboard"
      },
      setAdminToolbar() {
        this.toolbar = this.adminToolbar
        this.home = "/admindashboard"
      },
      setStandardToolbar() {
        this.toolbar = this.standardToolbar
        this.home = "/"
      },
      logout() {
        this.userinfo = null
        this.load_bar()
        this.goHome()
      },
      goHome() {
        router.push(this.home)
      }
    },
    beforeMount() {
      this.load_bar()
    }
  }
</script>

<style lang="stylus">
  @import './stylus/main'

  @require '../../node_modules/vuetify/src/stylus/settings/_colors'
 
  $theme := {
    primary: $red.darken-2
    accent: $red.accent-2
    secondary: $grey.lighten-1
    info: $blue.lighten-1
    warning: $amber.darken-2
    error: $red.accent-4
    success: $green.lighten-2
  }

</style>