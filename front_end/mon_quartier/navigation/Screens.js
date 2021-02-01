import React, { Component, useState } from "react";
import { Easing, Animated, Dimensions, View, Text, ScrollView, StyleSheet } from "react-native";

import { createStackNavigator } from "@react-navigation/stack";
import { createDrawerNavigator } from "@react-navigation/drawer";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";

import { Block, theme, Button as GaButton } from "galio-framework";

// screens
import Accueil from "../screens/Home";
import Onboarding from "../screens/Onboarding";
import Account from "../screens/Account";
import { token } from "../screens/Onboarding";
import Pro from "../screens/Pro";
import Profile from "../screens/Profile";
import Map from "../screens/Map";
import Register from "../screens/Register";
//import Elements from "../screens/Elements";
import Articles from "../screens/Articles";
import Input from '../components/Input';
// drawer
import CustomDrawerContent from "./Menu";

// header for screens
import { Icon, Header, Button } from "../components";
import { argonTheme, tabs, articles } from "../constants";
import csvjson from '../constants/csvjson';

const { width } = Dimensions.get("screen");

const Stack = createStackNavigator();
const Drawer = createDrawerNavigator();
const Tab = createBottomTabNavigator();


class Elementss extends React.Component {

  renderButtons = () => {
    const { navigation } = this.props;
    var id;

  };

  renderText = () => {
    return (
      <Block flex style={styles.group}>
        <Text bold size={16} style={styles.title}>
          Typography
        </Text>
        <Block style={{ paddingHorizontal: theme.SIZES.BASE }}>
          <Text
            h1
            style={{ marginBottom: theme.SIZES.BASE / 2 }}
            color={argonTheme.COLORS.DEFAULT}
          >
            Heading 1
          </Text>
          <Text
            h2
            style={{ marginBottom: theme.SIZES.BASE / 2 }}
            color={argonTheme.COLORS.DEFAULT}
          >
            Heading 2
          </Text>
          <Text
            h3
            style={{ marginBottom: theme.SIZES.BASE / 2 }}
            color={argonTheme.COLORS.DEFAULT}
          >
            Heading 3
          </Text>
          <Text
            h4
            style={{ marginBottom: theme.SIZES.BASE / 2 }}
            color={argonTheme.COLORS.DEFAULT}
          >
            Heading 4
          </Text>
          <Text
            h5
            style={{ marginBottom: theme.SIZES.BASE / 2 }}
            color={argonTheme.COLORS.DEFAULT}
          >
            Heading 5
          </Text>
          <Text
            p
            style={{ marginBottom: theme.SIZES.BASE / 2 }}
            color={argonTheme.COLORS.DEFAULT}
          >
            Paragraph
          </Text>
          <Text muted>This is a muted paragraph.</Text>
        </Block>
      </Block>
    );
  };


  renderTableCell = () => {
    const { navigation } = this.props;
    return (
      <Block flex style={styles.group}>
        <Text bold size={16} style={styles.title}>
          Table Cell
        </Text>
        <Block style={{ paddingHorizontal: theme.SIZES.BASE }}>
          <Block style={styles.rows}>
            <TouchableOpacity onPress={() => navigation.navigate("Pro")}>
              <Block row middle space="between" style={{ paddingTop: 7 }}>
                <Text size={14}>Manage Options</Text>
                <Icon
                  name="chevron-right"
                  family="entypo"
                  style={{ paddingRight: 5 }}
                />
              </Block>
            </TouchableOpacity>
          </Block>
        </Block>
      </Block>
    );
  };

  renderSocial = () => {
    return (
      <Block flex style={styles.group}>
        <Text bold size={16} style={styles.title}>
          Social
        </Text>
        <Block style={{ paddingHorizontal: theme.SIZES.BASE }}>
          <Block row center space="between">
            <Block flex middle right>
              <GaButton
                round
                onlyIcon
                shadowless
                icon="facebook"
                iconFamily="Font-Awesome"
                iconColor={theme.COLORS.WHITE}
                iconSize={theme.SIZES.BASE * 1.625}
                color={theme.COLORS.FACEBOOK}
                style={[styles.social, styles.shadow]}
              />
            </Block>
            <Block flex middle center>
              <GaButton
                round
                onlyIcon
                shadowless
                icon="twitter"
                iconFamily="Font-Awesome"
                iconColor={theme.COLORS.WHITE}
                iconSize={theme.SIZES.BASE * 1.625}
                color={theme.COLORS.TWITTER}
                style={[styles.social, styles.shadow]}
              />
            </Block>
            <Block flex middle left>
              <GaButton
                round
                onlyIcon
                shadowless
                icon="dribbble"
                iconFamily="Font-Awesome"
                iconColor={theme.COLORS.WHITE}
                iconSize={theme.SIZES.BASE * 1.625}
                color={theme.COLORS.DRIBBBLE}
                style={[styles.social, styles.shadow]}
              />
            </Block>
          </Block>
        </Block>
      </Block>
    );
  };

  renderNavigation = () => {
    return (
      <Block flex style={styles.group}>
        <Text bold size={16} style={styles.title}>
          Navigation
        </Text>
        <Block>
          <Block style={{ marginBottom: theme.SIZES.BASE }}>
            <Header 
              back 
                title="Title" navigation={this.props.navigation} />
          </Block>

          <Block style={{ marginBottom: theme.SIZES.BASE }}>
            <Header 
              tabs={tabs.categories} 
              search 
              title="Title" 
              navigation={this.props.navigation} />
          </Block>

          <Block style={{ marginBottom: theme.SIZES.BASE }}>
            <Header
              options
              search
              title="Title"
              optionLeft="Option 1"
              optionRight="Option 2"
              navigation={this.props.navigation}
            />
          </Block>
        </Block>
      </Block>
    );
  };

  render() {
    return (
      <Block flex center>
        <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={{ paddingBottom: 30, width }}>
          {this.renderButtons()}
        </ScrollView>
      </Block>
    );
  }
}


function searchStack(props) {
  return (
    <Stack.Navigator mode="card" headerMode="screen">
      <Stack.Screen
        name="Elements"
        component={Elements}
        options={{
          header: ({ navigation, scene }) => (
            <Header 
              title="Recherche" 
              navigation={navigation} 
              scene={scene} 
              back
            />
          ),
          cardStyle: { backgroundColor: "#F8F9FE" }
        }}
      />
    </Stack.Navigator>
  );
}


function SearchResults() {
var ABC = <Button onPress = {() => navigation.navigate('Profile')} color="secondary" textStyle={{ color: "black", fontSize: 12, fontWeight: "700" }} style={styles.button}> Panda WOK </Button>

for (let i = 0; i < 5; i++){  
  ABC = ABC + large
  }
return(ABC)
}


function sendSearchRequest(search,route){
  const url = new URL(route, 'http://localhost:5000/')
  url.searchParams.append('search',search)

  fetch(url, {
    method : 'GET'
  }).then((response) => response.json()).catch(
    (e) => {alert('Something went wrong' + e.message)}
  )
}


function Elements ({navigation}){
  var [search, setSearch] = useState('') ;
  var resultat='' ;

  return (
    <Block>
      <Input
        right
        onChangeText={(text) => setSearch(text)}
        search = {search}

        resultat = {sendSearchRequest(search,"commerce")}
        //onChangeText={
        //  (text) => setSearch(text),}
        //text = {text}
        //onChangeText={() => console.log('gg')}
        
        color="black"
        style={styles.search}
        placeholder="Que recherchezzzz vous?"
        placeholderTextColor={'#8898AA'}
        //onFocus={() => navigation.navigate('Pro')}
        iconContent={<Icon size={16} color={theme.COLORS.MUTED} name="search-zoom-in" family="ArgonExtra" />}
      />
    
    <ScrollView>
    <Block flex>
      <Text bold size={16} style={styles.title}>
        Resultats
      </Text>
      <Block style={{ paddingHorizontal: theme.SIZES.BASE }}>
        <Block center>
          <Button
            id = '1'
            //onPress ={() => }
            onPress = {() => navigation.navigate('Profile')}
            color="secondary"
            textStyle={{ color: "black", fontSize: 12, fontWeight: "700" }}
            style={styles.button}
          >
            Panda
          </Button>

          

          <Button
            id = '2'
            onPress = {() => navigation.navigate('Profile', {text: 'hello'})}
            color="secondary"
            textStyle={{ color: "black", fontSize: 12, fontWeight: "700" }}
            style={styles.button}
          >
            Belam Coiffure
          </Button>
          <Button
            id = '3'
            onPress = {() => navigation.navigate({name: 'Profile', key: id})}
            color="secondary"
            textStyle={{ color: "black", fontSize: 12, fontWeight: "700" }}
            style={styles.button}
          >
            Boucherie Sanzot
          </Button>
          <Button
            id = '4'
            onPress = {() => navigation.navigate({name: 'Profile', key: id})}
            color="secondary"
            textStyle={{ color: "black", fontSize: 12, fontWeight: "700" }}
            style={styles.button}
          >
            Monoprix
          </Button>
          <Button
            id = '5'
            onPress = {() => navigation.navigate({name: 'Profile', key: id})}
            color="secondary"
            textStyle={{ color: "black", fontSize: 12, fontWeight: "700" }}
            style={styles.button}
          >
            A2pas
          </Button>
          <Button
            id = '5'
            onPress = {() => navigation.navigate({name: 'Profile', key: id})}
            color="secondary"
            textStyle={{ color: "black", fontSize: 12, fontWeight: "700" }}
            style={styles.button}
          >
            A2pas
          </Button>
          <Button
            id = '5'
            onPress = {() => navigation.navigate({name: 'Profile', key: id})}
            color="secondary"
            textStyle={{ color: "black", fontSize: 12, fontWeight: "700" }}
            style={styles.button}
          >
            A2pas
          </Button>
        </Block>
      </Block>
    </Block>
    </ScrollView>
    </Block>
  );

}


const Profile2 = ({text}) => {
  console.log(text)
  //console.log(route.params)
  //console.log(route.params.text)

  return (
    <View>
      <Text> First Screen </Text>
      <Text> First Screen </Text>
      <Text> First Screen </Text>

      <Text> First Screen </Text>
    </View>
  )
}

function ProfileStack(props){
    //console.log(props.route)
    //console.log(props.route.params)
    //console.log(props.route.params.item)
    //const {item} = props.route.params.item;
    return(
      <Stack.Navigator initialRouteName="Profile" mode="card" headerMode="screen">
      <Stack.Screen
        name="Profile"
        component={Profile}
        id = {this.props}
        
        //item = {this.props}
        initialParams={{id : articles[1]} }
        options={{
          header: ({ navigation, scene }) => (
            <Header
              transparent
              white
              title="Profile"
              navigation={navigation}
              scene={scene}
            />
          ),
          cardStyle: { backgroundColor: "#FFFFFF" },
          headerTransparent: true
        }}
      />
    </Stack.Navigator>
    );
    }





function MapStack(props) {
  return (
    <Stack.Navigator initialRouteName="Map" mode="card" headerMode="screen">
      <Stack.Screen
        name="Map"
        component={Map}
        options={{
          header: ({ navigation, scene }) => (
            <Header
              transparent
              title="Map"
              navigation={navigation}
              scene={scene}
            />
          ),
          cardStyle: { backgroundColor: "#F8F9FE" }
        }}
      />

    </Stack.Navigator>
  );
}



function HomeStack(props) {
  console.log(token);
  console.log('couccou');
  return (
    <Stack.Navigator mode="card" headerMode="screen">
      <Stack.Screen
        name="Accueil"
        component={Articles}
        options={{
          header: ({ navigation, scene }) => (
            <Header
              transparent
              title="Accueil"
              search
              //options
              navigation={navigation}
              scene={scene}
            />
          ),
          cardStyle: { backgroundColor: "#F8F9FE" }
        }}
      />

    </Stack.Navigator>
  );
}

export default function OnboardingStack(props) {
  return (
    <Stack.Navigator mode="card" headerMode="none">
      <Stack.Screen
        name="Onboarding"
        component={Onboarding}
        option={{
          headerTransparent: true
        }}
      />
      <Stack.Screen name="App" component={AppStack} />
      <Drawer.Screen name="Register" component={Register} />
    </Stack.Navigator>
  );
}

function AppStack(props) {
  return (
    <Drawer.Navigator
      style={{ flex: 1 }}
      drawerContent={props => <CustomDrawerContent {...props} />}
      drawerStyle={{
        backgroundColor: "white",
        width: width * 0.8
      }}
      drawerContentOptions={{
        activeTintcolor: "white",
        inactiveTintColor: "#000",
        activeBackgroundColor: "transparent",
        itemStyle: {
          width: width * 0.75,
          backgroundColor: "transparent",
          paddingVertical: 16,
          paddingHorizonal: 12,
          justifyContent: "center",
          alignContent: "center",
          alignItems: "center",
          overflow: "hidden"
        },
        labelStyle: {
          fontSize: 18,
          marginLeft: 12,
          fontWeight: "normal"
        }
      }}
      initialRouteName="Home"
    >
      <Drawer.Screen name="Home" component={HomeStack} />
      <Drawer.Screen name="Profile" component={ProfileStack} />
      <Drawer.Screen name="Elements" component={searchStack} />
      <Drawer.Screen name="Account" component={Account} />
      <Drawer.Screen name="Map" component={MapStack} />
    </Drawer.Navigator>
  );
}

const styles = StyleSheet.create({
  title: {
    paddingBottom: theme.SIZES.BASE,
    paddingHorizontal: theme.SIZES.BASE * 2,
    marginTop: 44,
    color: argonTheme.COLORS.HEADER
  },
  group: {
    paddingTop: theme.SIZES.BASE * 2
  },
  shadow: {
    shadowColor: "black",
    shadowOffset: { width: 0, height: 2 },
    shadowRadius: 4,
    shadowOpacity: 0.2,
    elevation: 2
  },
  button: {
    marginBottom: theme.SIZES.BASE,
    width: width - theme.SIZES.BASE * 2
  },
  optionsButton: {
    width: "auto",
    height: 34,
    paddingHorizontal: theme.SIZES.BASE,
    paddingVertical: 10
  },
  input: {
    borderBottomWidth: 1
  },
  inputDefault: {
    borderBottomColor: argonTheme.COLORS.PLACEHOLDER
  },
  inputTheme: {
    borderBottomColor: argonTheme.COLORS.PRIMARY
  },
  inputInfo: {
    borderBottomColor: argonTheme.COLORS.INFO
  },
  inputSuccess: {
    borderBottomColor: argonTheme.COLORS.SUCCESS
  },
  inputWarning: {
    borderBottomColor: argonTheme.COLORS.WARNING
  },
  inputDanger: {
    borderBottomColor: argonTheme.COLORS.ERROR
  },
  social: {
    width: theme.SIZES.BASE * 3.5,
    height: theme.SIZES.BASE * 3.5,
    borderRadius: theme.SIZES.BASE * 1.75,
    justifyContent: "center"
  },
});