import React, { useState} from "react";
import {
  StyleSheet,
  Dimensions,
  ScrollView, 
  Image,
  ImageBackground,
  Platform,
  Linking
} from "react-native";
import { Block, Text, theme } from "galio-framework";
import { Button , Card} from "../components";
import { Images } from "../constants";
import { HeaderHeight } from "../constants/utils";

import server from "../constants/Server";
//import articles from "../constants/articles"

//MAP
import MapView, {PROVIDER_GOOGLE} from "react-native-maps";
import {RetroStyle} from "../constants/MapData";
import { useEffect } from "react";


function sendPromotionsRequest(updateFunction,route){
  const url = new URL(route, server.server)
  console.log(url)
  fetch(url, {
    method : 'GET'
  }).then((response) => response.json()).then(updateFunction).catch(
    (e) => {alert('Something went wrong' + e.message)}
  )
}

const { width, height } = Dimensions.get("screen");

const thumbMeasure = (width - 48 - 32) / 3;



export default function Profile(props) {

  COMMERCE = props.KOM;
  IMAGES = props.IMAGES;

  const ID = COMMERCE[0];
  const NOM = COMMERCE[1]
  const DESC = COMMERCE[2];
  const CITY = COMMERCE[3];
  const ZIP = COMMERCE[4];
  const ADDRESS = COMMERCE[5];
  const LATITUDE = COMMERCE[6];
  const LONGITUDE = COMMERCE[7];

  const URL = COMMERCE[8];
  

  var [promotions, setPromotions] = useState([])
  var [Pimages, setPimages] = useState([])
    
 
  function updateFunction(response){
    { 
      promotions = setPromotions(response['resultat'])
      Pimages = setPimages(response['images'])
      
      }
  }

  console.log(promotions)
  console.log(Pimages)
  const id = ID.toString()
  console.log(id)
    useEffect( ()=>{sendPromotionsRequest(updateFunction, "commerce/"+id+"/promotion");}, []);

  if (promotions.length == 0 ) {
  
    return(
        <Block center>
          <Text>pas d'articles</Text>
        </Block>
          )}

console.log(promotions)


  return (
    <Block flex style={ProfileStyles.profile}>
      <Block flex>
        <ImageBackground
          source={Images.ProfileBackground}
          style={ProfileStyles.profileContainer}
          imageStyle={ProfileStyles.profileBackground}
        >
          <ScrollView
            showsVerticalScrollIndicator={false}
            style={{ width, marginTop: '25%' }}
          >
            <Block flex style={ProfileStyles.profileCard}>
              <Block flex center>
              <MapView
                initialRegion={{
                  latitude: LATITUDE,
                  longitude: LONGITUDE,
                  latitudeDelta: 0.02864195044303443,
                  longitudeDelta: 0.020142817690068,
                }}
                provider={PROVIDER_GOOGLE}
                customMapStyle={RetroStyle}
                style={ProfileStyles.productMap}
                showsUserLocation={true}
                followsUserLocation={true}
              >
                
                    <MapView.Marker coordinate={{latitude: LATITUDE, longitude: LONGITUDE}}>
                      <Image
                        source={require('../assets/imgs/pin.png')}
                        style={ProfileStyles.marker}
                        resizeMode="contain"
                      />
                  </MapView.Marker>
                 
              </MapView>
            </Block>
              <Block middle style={ProfileStyles.avatarContainer}>

                <Block style={ProfileStyles.avatar}>
                  <Image

                    source={{ uri: 'http://localhost:5000/' + IMAGES[0] }}
                    flex
                    style={{margin:10}}
                    resizeMode="contain"
                  />

                </Block>
              </Block>
              <Block >
                <Block center>
                  <Text style={ProfileStyles.title}>
                    {NOM}
                  </Text>
                  <Text  style={ProfileStyles.description}>
                    {ADDRESS}, {ZIP}, {CITY}
                  </Text>
                </Block>
                <Block
                  middle
                  row
                  space="evenly"
                  style={{ marginTop: 10, paddingBottom: 0}}
                >
                  <Button
                    small
                    style={{ backgroundColor: "blue" }}
                    onPress={() =>
                        Linking.openURL(
                            URL
                          ).catch(err => console.error("An error occurred", err))
                    }
                  >
                    SITE WEB
                  </Button>
                  <Button
                    small
                    style={{ backgroundColor: "red" }}
                    onPress={() =>
                        Linking.openURL(
                          "https://www.google.com/maps/dir/?api=1&destination="+ADDRESS
                          ).catch(err => console.error("An error occurred", err))
                    }
                  >
                    ITINERAIRE
                  </Button>
                </Block>
                
              </Block>
              <Block flex>
                
                <Block middle style={{ marginTop: 20, marginBottom: 16 }}>
                  <Block style={ProfileStyles.divider} />
                </Block>
                <Block middle>
                  <Text
                    bold
                    size={16}
                    color="#525F7F"
                    style={{ textAlign: "center" }}
                  >
                  
                    {DESC}
                  </Text>
                  <Button
                    color="transparent"
                    textStyle={{
                      color: "#233DD2",
                      fontWeight: "500",
                      fontSize: 16
                    }}
                  >
                    Show more
                  </Button>
                </Block>
                <Block middle style={{ marginTop: 20, marginBottom: 16 }}>
                  <Block style={ProfileStyles.divider} />
                </Block>
               <Block>
                <Text style={ProfileStyles.promotionTitle}>
                  Promotions
                </Text>
                {promotions.map((promotion, index) => {
                  return(
                  <Block>
                    <Card item={promotion} im={Pimages} horizontal/>
                  </Block>);
                })}

               </Block>
              </Block>
            </Block>
          </ScrollView>
        </ImageBackground>
      </Block>
    </Block>
  );
}


const ProfileStyles = StyleSheet.create({
profile: {
  marginTop: Platform.OS === "android" ? -HeaderHeight : 0,
  // marginBottom: -HeaderHeight * 2,
  flex: 1
},
profileContainer: {
  width: width,
  height: height,
  padding: 0,
  zIndex: 1
},
profileBackground: {
  width: width,
  height: height
},
profileCard: {
  //position: "relative",
  padding: theme.SIZES.BASE,
  marginHorizontal: theme.SIZES.BASE,
  marginTop: 100,
  borderTopLeftRadius: 6,
  borderTopRightRadius: 6,
  backgroundColor: theme.COLORS.WHITE,
  shadowColor: "black",
  shadowOffset: { width: 0, height: 0 },
  shadowRadius: 8,
  shadowOpacity: 0.2,
  zIndex: 2
},
info: {
  paddingHorizontal: 40
},
avatarContainer: {
  position: "relative",
  marginTop: -80,
  shadowColor: "black",
  shadowOffset: { width: 0, height: 0 },
  shadowRadius: 30,
  shadowOpacity: 0.2,

},
avatar: {
  width: 200,
  height: 150,
  borderRadius: 50,
  
  backgroundColor: "white",
  margin:10,

},
nameInfo: {
  marginTop: 5
},
divider: {
  width: "90%",
  borderWidth: 1,
  borderColor: "#E9ECEF"
},
thumb: {
  borderRadius: 4,
  marginVertical: 4,
  alignSelf: "center",
  width: thumbMeasure,
  height: thumbMeasure
}, 
title:{
  fontSize: 30,
  color:"#32325D"
},
description:{
  fontSize: 10,
  marginTop: 5, 
},
productMap: {
  width: width-30,
  height: 200,
  borderRadius: 10,
  marginTop:-20,
  marginHorizontal:10

},
marker: {
  width: 50,
  height: 50,
},
promotionTitle:{
  fontSize:20,
  fontWeight: "500",
  marginLeft:theme.SIZES.BASE
}
});

export {ProfileStyles}

