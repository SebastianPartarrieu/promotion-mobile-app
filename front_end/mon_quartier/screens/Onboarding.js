import React, {useState} from "react";
import {
  StyleSheet,
  ImageBackground,
  Dimensions,
  StatusBar,
  KeyboardAvoidingView,
  TextInput
} from "react-native";
import { Block, Checkbox, Text, theme } from "galio-framework";

import { Button, Icon, Input } from "../components";
import { Images, argonTheme } from "../constants";
import { string } from "prop-types";

const { width, height } = Dimensions.get("screen");

const { token } = 'None';


function sendLoginRequest(username,password,updateFunction,route){
  const url = new URL(route, 'http://localhost:5000/')
  url.searchParams.append('clemail',username)
  url.searchParams.append('clmdp',password)
  fetch(url, {
    method : 'GET'
  }).then((response) => response.json()).then(updateFunction).catch(
    (e) => {alert('Something went wrong' + e.message)}
  )
}




function Onboarding({ navigation }){

    function updateFunction(response){
      {response = 401?
      console.log(response):
        navigation.navigate("App"),
        token = {reponse} }
    }


    const [username, setUsername] = useState('email') ;
    const [password, setPassword] = useState('mdp') ;
    //console.log(password)


    return (
      <Block flex middle>
      <StatusBar hidden />
      <ImageBackground
        source={Images.RegisterBackground}
        style={{ width, height, zIndex: 1 }}
      >
        <Block flex middle>
          <Block style={styles.registerContainer}>
            <Block flex>
              <Block flex={0.10} middle style={{marginTop:100, marginBottom: 50 }} >
                <Text color="#8898AA" size={30} >
                  Connectez vous !
                </Text>
              </Block>
              <Block flex center>
                <KeyboardAvoidingView
                  style={{ flex: 1 }}
                  behavior="padding"
                  enabled
                >
                  
                  <Block width={width * 0.8} style={{marginTop:35, marginBottom: 15 }}>
                    <Input
                      onChangeText={(text) => setUsername(text)}
                      username = { username }
                      
                      borderless
                      placeholder="Email"
                      iconContent={
                        <Icon
                          size={16}
                          color={argonTheme.COLORS.ICON}
                          name="ic_mail_24px"
                          family="ArgonExtra"
                          style={styles.inputIcons}
                        />
                      }
                    />
                  </Block>
                  <Block width={width * 0.8}>
                    <Input
                      onChangeText={(text) => setPassword(text)}
                      password = { password }
                      id='password'
                      password
                      borderless
                      placeholder="Mot de passe"
                      iconContent={
                        <Icon
                          size={16}
                          color={argonTheme.COLORS.ICON}
                          name="padlock-unlocked"
                          family="ArgonExtra"
                          style={styles.inputIcons}
                        />
                      }
                    />
                  </Block>
                  
                  <Block middle>
                    <Button color="primary" style={styles.createButton}
                    //onPress={() => navigation.navigate("App")}> 
                    onPress={() => sendLoginRequest(username,password,updateFunction,'login')}>
                    
                      <Text bold size={14} color={argonTheme.COLORS.WHITE}>
                        CONNEXION
                      </Text>
                    </Button>
                  </Block>
                  <Block middle>
                  <Button
                        color="transparent"
                        textStyle={{
                          color: argonTheme.COLORS.PRIMARY,
                          fontSize: 14
                          
                        }}
                        onPress={() => navigation.navigate("App")}>
                      
                        Créer son compte
                      </Button>
                  </Block>
                </KeyboardAvoidingView>
              </Block>
            </Block>
          </Block>
        </Block>
      </ImageBackground>
    </Block>
  );
}



const styles = StyleSheet.create({
registerContainer: {
  width: width * 0.9,
  height: height * 0.78,
  backgroundColor: "#F4F5F7",
  borderRadius: 4,
  shadowColor: argonTheme.COLORS.BLACK,
  shadowOffset: {
    width: 0,
    height: 4
  },
  shadowRadius: 8,
  shadowOpacity: 0.1,
  elevation: 1,
  overflow: "hidden"
},
socialConnect: {
  backgroundColor: argonTheme.COLORS.WHITE,
  borderBottomWidth: StyleSheet.hairlineWidth,
  borderColor: "#8898AA"
},
socialButtons: {
  width: 120,
  height: 40,
  backgroundColor: "#fff",
  shadowColor: argonTheme.COLORS.BLACK,
  shadowOffset: {
    width: 0,
    height: 4
  },
  shadowRadius: 8,
  shadowOpacity: 0.1,
  elevation: 1
},
socialTextButtons: {
  color: argonTheme.COLORS.PRIMARY,
  fontWeight: "800",
  fontSize: 14
},
inputIcons: {
  marginRight: 12
},
passwordCheck: {
  paddingLeft: 15,
  paddingTop: 13,
  paddingBottom: 30
},
createButton: {
  width: width * 0.5,
  marginTop: 25
}
});
export default Onboarding;
