import React, {useEffect, useState} from "react";
import { useSafeArea } from "react-native-safe-area-context";
import {
  ScrollView,
  StyleSheet,
  Image,
  Button
} from "react-native";
import { Block, Text, theme } from "galio-framework";

import Images from "../constants/Images";
import { DrawerItem as DrawerCustomItem } from '../components';




function sendArticlesRequest(updateFunction,route){
  const url = new URL(route, 'http://0.0.0.0:5000/')


  fetch(url, {
    method : 'GET'
  }).then((response) => response.json()).then(updateFunction).catch(
    (e) => {alert('Something went wrong' + e.message)}
  )
}



function CustomDrawerContent({ drawerPosition, navigation, profile, focused, state, ...rest }) {
  
  
  
  
  var [articles, setArticles] = React.useState([])
  function updateFunction(response){
    { 
      articles = setArticles(response['resultat'])
      
      }
  }
  
  useEffect( ()=>{sendArticlesRequest(updateFunction, "commerce");}, []);




    

  const insets = useSafeArea();
  const screens = [
    "Accueil", 
    "Profile",
    "Elements",
    "Map",
  ];
  return (
    <Block
      style={styles.container}
      forceInset={{ top: 'always', horizontal: 'never' }}
    >
      <Block flex={0.06} style={styles.header}>
        <Image styles={styles.logo} source={Images.Logo} />
      </Block>
      <Block flex style={{ paddingLeft: 8, paddingRight: 14 }}>
        <ScrollView style={{ flex: 1 }} showsVerticalScrollIndicator={false}>
          {screens.map((item, index) => {
              return (
                <Block>
                <DrawerCustomItem
                  title={item}
                  key={index}
                  navigation={navigation}
                  focused={state.index === index ? true : false}
                />
                <Button 
                  title='hey'
                  onPress={() => navigation.navigate('Map', {comm : articles})}>
                </Button>
                </Block>
              );
            })}
            <Block flex style={{ marginTop: 24, marginVertical: 8, paddingHorizontal: 8 }}>
              <Block style={{ borderColor: "rgba(0,0,0,0.2)", width: '100%', borderWidth: StyleSheet.hairlineWidth }}/>
              <Text color="#8898AA" style={{ marginTop: 16, marginLeft: 8 }}>DOCUMENTATION</Text>
            </Block>
            <DrawerCustomItem title="Getting Started" navigation={navigation} />
        </ScrollView>
      </Block>
    </Block>
  );
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    paddingHorizontal: 28,
    paddingBottom: theme.SIZES.BASE,
    paddingTop: theme.SIZES.BASE * 3,
    justifyContent: 'center'
  }
});

export default CustomDrawerContent;
