<template>
    <div>
        <v-app-bar fixed color="#47A0F6">
            <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon>
            <v-toolbar-title>特定警察</v-toolbar-title>
            <v-spacer></v-spacer>
        </v-app-bar>
        <v-navigation-drawer v-model="drawer" fixed temporary color="#F2F7FF">
            <v-list nav dense>
                <v-list-item-group active-class="deep-purple--text text--accent-4">
                    <v-list-item v-for="(menuItem, index) in menuItems" :key=index>
                        <v-list-item-icon>
                            <v-icon>{{menuItem.icon}}</v-icon>
                        </v-list-item-icon>
                        <v-list-item>
                            <a v-if="menuItem.name=='Home'" v-bind:href="`${menuItem.link}`">{{menuItem.name}}</a>
                            <a v-else v-bind:href="`${menuItem.link}`" target="_blank">{{menuItem.name}}</a>
                        </v-list-item>
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
                    name: "Home",
                    link: "/",
                },{
                    icon: "mdi-twitter",
                    name: "Twitter",
                    link: "https://www.twitter.com",
                },{
                    icon: "mdi-instagram",
                    name: "Instagram",
                    link: "https://www.instagram.com",
                },{
                    icon: "mdi-facebook",
                    name: "Facebook",
                    link: "https://www.facebook.com",
                }],
            }
        }
    }
</script>