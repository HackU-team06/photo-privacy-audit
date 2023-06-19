<template>
    <div>
        <v-app-bar fixed color="grey lighten-5">
            <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon>
            <v-toolbar-title>PrivacyChecker</v-toolbar-title>
            <v-spacer></v-spacer>
        </v-app-bar>
        <v-navigation-drawer v-model="drawer" fixed temporary>
            <v-list nav dense>
                <v-list-item-group v-model="group" active-class="deep-purple--text text--accent-4">
                    <v-list-item v-for="(menuItem, index) in menuItems" :key=index>
                        <v-list-icon>
                            <v-icon>{{menuItem.icon}}</v-icon>
                        </v-list-icon>
                        <v-list-tile>
                            <a v-if="menuItem.name=='home'" v-bind:href="`${menuItem.link}`">{{menuItem.name}}</a>
                            <a v-else v-bind:href="`${menuItem.link}`" target="_blank">{{menuItem.name}}</a>
                        </v-list-tile>
                    </v-list-item>
                </v-list-item-group>
            </v-list>
        </v-navigation-drawer>
    </div>
</template>

<script>
    export default{
        data(){
            return{
                drawer: false,
                menuItems: [
                {
                    icon: "mdi-home",
                    name: "home",
                    link: "/",
                },{
                    icon: "mdi-yahoo",
                    name: "Yahoo!",
                    link: "https://www.yahoo.co.jp",
                },{
                    icon: "mdi-twitter",
                    name: "twitter!",
                    link: "https://www.twitter.com",
                },{
                    icon: "mdi-github",
                    name: "github",
                    link: "https://www.github.com",
                },]
            }
        },
        methods:{
            
        }
    }
</script>