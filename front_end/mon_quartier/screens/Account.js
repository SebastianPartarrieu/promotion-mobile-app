import React, {useState} from "react";
import {
  StyleSheet,
  ImageBackground,
  Dimensions,
  StatusBar,
  KeyboardAvoidingView
} from "react-native";
import { Block, Checkbox, Text, theme } from "galio-framework";
import { token } from "./Onboarding";
import { Button, Icon, Input } from "../components";
import { Images, argonTheme } from "../constants";
import { string } from "prop-types";
import Onboarding from "./Onboarding";

const { width, height } = Dimensions.get("screen");




function getInfos(token,updateFunction,route){

  const url = new URL(route, 'http://localhost:5000/')

  url.searchParams.append('token',token)



  fetch(url, {
    method : 'GET'
  }).then((response) => response.json()).then(updateFunction).catch(
    (e) => {alert('Something went wrong' + e.message)}
  )
}




function Account({navigation}){

  const [lastname, setLastname] = useState('nom') ;
  const [firstname, setFirstname] = useState('prenom') ;
  const [city, setCity] = useState('');
  
  const [username, setUsername] = useState('email') ;
  const [password, setPassword] = useState('mdp') ;

  function updateFunction(response){
      { console.log(response)
        response['is_registered']?(
          navigation.navigate("Onboarding")
        ):
        (
          console.log(firstname)
        )
          
        
        }
    }
    return (
      <Block flex middle>
        <StatusBar hidden />
        <ImageBackground
          //source={Images.Bacdkground}
          style={{ width, height, zIndex: 1 }}
        >
          <Block flex middle>
            <Block style={styles.registerContainer}>
              <Block flex>
                <Block flex center>
                  <KeyboardAvoidingView
                    style={{ flex: 1 }}
                    behavior="padding"
                    enabled
                  >
                    <Block width={width * 0.8} style={{ marginBottom: 15 }}>
                      <Input
                      
                        onChangeText={(text) => setLastname(text)}
                        lastname = { lastname }
                        borderless
                        placeholder="Nom"
                        iconContent={
                          <Icon
                            size={16}
                            color={argonTheme.COLORS.ICON}
                            name="hat-3"
                            family="ArgonExtra"
                            style={styles.inputIcons}
                          />
                        }
                      />
                    </Block>
                    <Block width={width * 0.8} style={{ marginBottom: 15 }}>
                      <Input
                        borderless
                        onChangeText={(text) => setFirstname(text)}
                        firstname = { firstname }
                        placeholder="Prénom"
                        iconContent={
                          <Icon
                            size={16}
                            color={argonTheme.COLORS.ICON}
                            name="hat-3"
                            family="ArgonExtra"
                            style={styles.inputIcons}
                          />
                        }
                      />
                    </Block>
                    <Block width={width * 0.8} style={{ marginBottom: 15 }}>
                      <Input
                        borderless
                        onChangeText={(text) => setUsername(text)}
                        username = { username }
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
                        id='password'
                        password
                        borderless
                        onChangeText={(text) => setPassword(text)}
                        password = { password }
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
                    <Block row width={width * 0.75}>
                      <Checkbox
                        checkboxStyle={{
                          borderWidth: 3
                        }}
                        color={argonTheme.COLORS.PRIMARY}
                        label="J'accepte les conditions de"
                      />
                      <Button
                        style={{ width: 100 }}
                        color="transparent"
                        textStyle={{
                          color: argonTheme.COLORS.PRIMARY,
                          fontSize: 14
                        }}
                      >
                        confidentialité
                      </Button>
                    </Block>
                    <Block middle>
                      <Button 
                        color="primary" 
                        style={styles.createButton}
                        onPress={() => sendRegisterRequest(lastname,firstname,username,password,updateFunction,'signup')}>                        
                        <Text bold size={14} color={argonTheme.COLORS.WHITE}>
                          CRÉER MON COMPTE
                        </Text>
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

export default Account;
