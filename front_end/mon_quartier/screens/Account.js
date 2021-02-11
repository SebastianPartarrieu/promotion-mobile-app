import React, {useEffect, useState} from "react";
import {
  StyleSheet,
  ImageBackground,
  Dimensions,
  StatusBar,
  KeyboardAvoidingView
} from "react-native";

import DropDownPicker from 'react-native-dropdown-picker';

import { Block, Text } from "galio-framework";
import { token } from "./Onboarding";
import { Button, Icon, Input, Header } from "../components";
import { argonTheme } from "../constants";


import server from "../constants/Server";
import cities from "../constants/cities"
import { DrawerContentScrollView } from "@react-navigation/drawer";

const { width, height } = Dimensions.get("screen");







function Account({navigation}){


  var [lastname, setLastname] = useState('nom') ;
  const [firstname, setFirstname] = useState('prenom') ;

  const [city, setCity] = useState('');
  
  const [username, setUsername] = useState('email') ;
  const [password, setPassword] = useState('mdp') ;



  function updateFunction(response){
      { 
        setLastname(response['resultat'][0][0])  
        setFirstname(response['resultat'][0][1]) 
        setUsername(response['resultat'][0][2]) 
        setCity(response['resultat'][0][3]) 
        }
    }



    function getInfos(token,updateFunction,route){

      const url = new URL(route, server.server)
    
      url.searchParams.append('token',token)
      fetch(url, {
        method : 'GET'
      }).then((response) => response.json()).then(updateFunction).catch(
        (e) => {alert('Something went wrong' + e.message)}
      )
    }


    function changeInfos(token,lastname,firstname,username,city_id,route){
      const url = new URL(route, server.server)
    
      url.searchParams.append('token',token)
      url.searchParams.append("clnom",lastname)
      url.searchParams.append("clpnom",firstname)
      url.searchParams.append("clemail",username)
      url.searchParams.append("aid",city_id)

      fetch(url, {method : 'PATCH'})

    
    }


    useEffect( ()=>{getInfos(token,updateFunction,'myclient')}, []);

    return (
      <Block flex middle>

        <StatusBar hidden />
        <ImageBackground
          //source={Images.Bacdkground}
          style={{ width, height, zIndex: 1 }}
        >
          <Header 
              title="Mon compte" 
              navigation={navigation} 
              back
              //transparent
              //scene={scene} 
              //search
            />
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
                        defaultValue = {lastname}
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
                        defaultValue = {firstname}
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
                    <Block width={width * 0.8} style={{ marginBottom: 0 }}>
                      <Input
                        borderless

                        defaultValue = {username}
          
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
                    <Block width={width * 0.8} style={{ marginBottom: 15 }}>
                      

                     
                    </Block>

                    <Block width={width * 0.8} style={{ marginBottom: 15 }}>

                    </Block>


                    <Block width={width * 0.8} style = {{ marginBottom: 150}}>

                    <DropDownPicker
                          items= {cities}

                          defaultValue={'1'}
                          containerStyle={{height: 40}}
                          style={{
                            backgroundColor: '#FFFFFF',
                            color:'#000000'}}
                          //style={{backgroundColor: '#0000'}}
                          itemStyle={{
                            justifyContent: 'flex-start'
                            }}
                          dropDownStyle={{backgroundColor: '#FFFFFF'}}
                          onChangeItem={item => setCity(item.value)}
                          //city = {city}
                          labelStyle={{
                            fontSize: 14,
                            textAlign: 'left',
                            color: '#000'
                            }}
                        />

                    </Block>
                    <Block middle>
                      <Button 
                        color="primary" 
                        style={styles.createButton}
                        onPress={() => changeInfos(token,lastname,firstname,username,city,"/myclient")}>               
                        <Text bold size={14} color={argonTheme.COLORS.WHITE}>
                          Enregistrer
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
