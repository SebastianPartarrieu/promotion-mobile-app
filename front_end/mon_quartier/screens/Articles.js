import React, { Component, useState } from "react";
import {
  ScrollView,
  StyleSheet,
  Image,
  TouchableWithoutFeedback,
  ImageBackground,
  Dimensions,
  View,
  TouchableOpacity,
  Button,
  Animated
} from "react-native";
//galio
import { Block, Text, theme } from "galio-framework";
//argon
import { Images, argonTheme, articles } from "../constants/";
import { Card } from "../components/";
import MapView, {Marker, PROVIDER_GOOGLE} from "react-native-maps";
import {RetroStyle} from "../constants/MapData";
import Ionicons from 'react-native-vector-icons/Ionicons';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import Fontisto from 'react-native-vector-icons/Fontisto'
import { useEffect } from "react";
import Geolocation from '@react-native-community/geolocation';
import server from "../constants/Server";
function sendSearchRequest(search,categorie,updateFunction,route){

  const url = new URL(route, server.server)

  const recherche = search;
  url.searchParams.append('search',recherche)
  if (categorie!='')
    { 
      url.searchParams.append('categorie',categorie)
    };
  

  fetch(url, {
    method : 'GET',
    headers: {
      Accept: 'application/json',},

  }).then((response) => response.json()).then(updateFunction).catch(
    (e) => {alert('Something went wrong' + e.message)}
  )
}


const { width } = Dimensions.get("screen");

const thumbMeasure = (width - 48 - 32) / 3;
const cardWidth = width - theme.SIZES.BASE * 2;


/// Requete serveur
function sendArticlesRequest(updateFunction,route){
  const url = new URL(route, server.server)

  fetch(url, {
    method : 'GET'
  }).then((response) => response.json()).then(updateFunction).catch(
    (e) => {alert('Something went wrong ' + e.message)}
  )
}

var k=0;

// Screen accueil
function Articles(props) {

    var [articles, setArticles] = React.useState([])
    var [images, setImages] = useState([])
    var [userloc, setUserloc] = useState([{latitude: 0, longitude: 0}])

    useEffect(()=>{Geolocation.getCurrentPosition((info) => setUserloc(info.coords))},[]); 
    //console.log(userloc.latitude)

    function ArticlesupdateFunction(response){
      { 
        articles = setArticles(response['resultat'])
        images = setImages(response['images'])
        }
    }
    k=1;

    
 
    
  useEffect(()=>{sendSearchRequest('','', ArticlesupdateFunction, "commerce");}, []);
  if (articles.length == 0 ) {
  return(
      <Block center>
        <Text>pas d'articles</Text>
      </Block>
        )}




  // suggestions en haut
    var suggestions = [];
    function Suggest(){
      var buffer = [];
      var n = 3;

      for(var iter = 0; iter < n; iter++){
        

        const id = iter;
        const DISTANCE = Distance(userloc.latitude, userloc.longitude, articles[id][6], articles[id][7]).toString().substring(0,4)+"0"
        buffer.push(
          <Block style={styles.productItem} key={id} >     
            <Card item={articles[id]} im ={images[id]} distance = {DISTANCE}
 full />
          </Block>
        )
      }
      return(buffer)
    }

    function deg2rad(deg) {
      return (deg * Math.PI)/180
    }
    function Distance(lat1,lng1,lat2,lng2) {
      var R = 6371; // Radius of the earth in km
      var dLat = deg2rad(lat2-lat1);  // deg2rad below
      var dLon = deg2rad(lng2-lng1); 
      var a = 
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * 
        Math.sin(dLon/2) * Math.sin(dLon/2)
        ; 
      var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
      var d = R * c; // Distance in km
      return d;
    }
   


  // scroll view en bas
    function SmallSlide({category}){
      var buffer = [];
      var n = articles.length;
   
      if (category=='Tous'){
        for(var iter = 0; iter < n; iter++){
          const id = iter;
          const DISTANCE = Distance(userloc.latitude, userloc.longitude, articles[id][6], articles[id][7]).toString().substring(0,4)+"0"     
          buffer.push(
          <Block 
            style={styles.productScroll}
            key={id}>
            <Card 
              item={articles[id]}
              im = {images[id]}
              distance = {DISTANCE}/>
          </Block>)
          }}

      else{
        for(var iter = 0; iter < n; iter++){
          const id = iter;
          if (articles[id][9]==category){
            const DISTANCE = Distance(userloc.latitude, userloc.longitude, articles[id][6], articles[id][7]).toString().substring(0,4)+"0"
          buffer.push(
            <Block 
              style={styles.productScroll}
              key={id}>
              <Card 
                item={articles[id]}
                im = {images[id]}
                distance = {DISTANCE}/>
            </Block>)
            }}}
      return(buffer)
  }

    //Animations
    const entranceAnimation = new Animated.Value(0);
      Animated.timing(entranceAnimation, {
        toValue: 100,
        duration: 1800,
        useNativeDriver: true
      }).start()

  //useEffect( ()=>{componentDidMount();}, []);

 //Categories 
 const categories =  [
  {
    name: 'Restaurant',
    icon: <Ionicons name="ios-restaurant" style={styles.chipsIcon} size={18} />,
  },
  {
    name: 'Coiffeur',
    icon: <Ionicons name="md-restaurant" style={styles.chipsIcon} size={18} />,
  },
  {
    name: 'Textile',
    icon: <MaterialCommunityIcons name="food" style={styles.chipsIcon} size={18} />,
  },
  {
    name: 'Epicerie',
    icon: <Fontisto name="hotel" style={styles.chipsIcon} size={15} />,
  },
  {
    name: 'Boulangerie',
    icon: <Fontisto name="hotel" style={styles.chipsIcon} size={15} />,
  },
  {
    name: 'Autre',
    icon: <Fontisto name="hotel" style={styles.chipsIcon} size={15} />,
  },
  {
    name: 'Jeux',
    icon: <Fontisto name="hotel" style={styles.chipsIcon} size={15} />,
  }
  ]
    
  


    const { navigation } = props;
    return (
      <Block flex center>
        <ScrollView
          showsVerticalScrollIndicator={false}
        >
        <Block flex style={styles.group}>
        
        <Text bold size={26} style={styles.title}>
          Suggestions
        </Text>
        <Block flex >
            <Animated.ScrollView
              horizontal={true}
              pagingEnabled={true}
              decelerationRate={0}
              scrollEventThrottle={16}
              snapToAlignment="center"
              showsHorizontalScrollIndicator={true}
              style={{transform: [{translateY: entranceAnimation.interpolate({
                inputRange: [0, 100],
                outputRange: [-1000, 0] 
              })}]}}
              snapToInterval={cardWidth + theme.SIZES.BASE * 0.375}
              contentContainerStyle={{
              paddingHorizontal: theme.SIZES.BASE / 2
              }}
            >
            <Suggest/>
            </Animated.ScrollView>
          </Block>
          <Text bold size={26} style={styles.title}>
          Autour de vous
        </Text>
          <Block flex center>
            <Animated.View style={{transform: [{translateX: entranceAnimation.interpolate({
                inputRange: [40, 100],
                outputRange: [1000, 0] 
              })}]}}>
              <MapView
                initialRegion={{
                  latitude: articles[0][6],
                  longitude: articles[0][7],
                  latitudeDelta: 0.02864195044303443,
                  longitudeDelta: 0.020142817690068,
                }}
                provider={PROVIDER_GOOGLE}
                customMapStyle={RetroStyle}
                style={styles.productMap}
                onPress={() => navigation.navigate('Map', {comm : articles, imm: images})}
                showsUserLocation={true}
                followsUserLocation={true}
              >
                {articles.map((marker, index) => {
              
                  return (
                    <MapView.Marker 
                      key={index}
                      coordinate={{latitude: marker[6], longitude: marker[7]}}>
                      <Image
                        
                        source={require('../assets/imgs/pin.png')}
                        style={styles.marker}
                        resizeMode="contain"
                      />
                  </MapView.Marker>
                  );
                })}
              </MapView>
            </Animated.View>
          </Block>
        <Text bold size={26} style={styles.title}>
          Catégories
        </Text>
        
        <Block flex>
        <Text bold size={16} style={styles.subtitle}>
                    Tous
                  </Text>
          <Animated.ScrollView
            horizontal
            scrollEventThrottle={1}
            showsHorizontalScrollIndicator={false}
            style={{transform: [{translateX: entranceAnimation.interpolate({
              inputRange: [80, 100],
              outputRange: [1000, 0] 
            })}]}}
            //style={styles.chipsScrollView}
            contentInset={{ // iOS only
              top:0,
              left:0,
              bottom:0,
              right:20
            }}
            contentContainerStyle={{
              paddingRight: Platform.OS === 'android' ? 20 : 0
            }}
          >

            <SmallSlide category='Tous' />
          </Animated.ScrollView>
              
        </Block>

              {categories.map((marker, index) => {
                //console.log(marker.name);

                return(

               <Block flex
               key= {index}
              >
                 <Text bold size={16} style={styles.subtitle}>
                    {marker.name}
                  </Text>
                  <Animated.ScrollView

                    horizontal
                    scrollEventThrottle={1}
                    showsHorizontalScrollIndicator={false}
                    style={{transform: [{translateX: entranceAnimation.interpolate({
                      inputRange: [80, 100],
                      outputRange: [1000, 0] 
                    })}]}}
                    //style={styles.chipsScrollView}
                    contentInset={{ // iOS only
                      top:0,
                      left:0,
                      bottom:0,
                      right:20
                    }}
                    contentContainerStyle={{
                      paddingRight: Platform.OS === 'android' ? 20 : 0
                    }}
                  >
                      
                  <SmallSlide category={marker.name}/>
                </Animated.ScrollView>
              </Block>
                )
            })}
        
        <Block flex>
          <Block style={{ paddingHorizontal: theme.SIZES.BASE }}>
            <Block flex row>
            </Block>           
          </Block>          
        </Block>
      </Block>
      </ScrollView>
      </Block>
    );
  };


const styles = StyleSheet.create({
  title: {
    paddingBottom: theme.SIZES.BASE,
    paddingHorizontal: theme.SIZES.BASE * 2,
    marginTop: 20,
    color: argonTheme.COLORS.HEADER
  },
  subtitle: {
    paddingBottom: theme.SIZES.BASE,
    paddingHorizontal: theme.SIZES.BASE * 2,
    marginTop: 5,
    marginBottom:-20,
    color: argonTheme.COLORS.HEADER
  },
  group: {
    paddingTop: theme.SIZES.BASE
  },
  albumThumb: {
    borderRadius: 4,
    marginVertical: 4,
    alignSelf: "center",
    width: thumbMeasure,
    height: thumbMeasure
  },
  category: {
    backgroundColor: theme.COLORS.WHITE,
    marginVertical: theme.SIZES.BASE / 2,
    borderWidth: 0
  },
  categoryTitle: {
    height: "100%",
    paddingHorizontal: theme.SIZES.BASE,
    backgroundColor: "rgba(0, 0, 0, 0.5)",
    justifyContent: "center",
    alignItems: "center"
  },
  imageBlock: {
    overflow: "hidden",
    borderRadius: 4
  },
  productItem: {
    width: cardWidth - theme.SIZES.BASE * 2,
    marginHorizontal: theme.SIZES.BASE,
    shadowColor: "black",
    shadowOffset: { width: 0, height: 7 },
    shadowRadius: 10,
    shadowOpacity: 0.2
  },
  productScroll: {
    width: cardWidth - theme.SIZES.BASE * 13,
    marginHorizontal: theme.SIZES.BASE,
    shadowColor: "black",
    shadowOffset: { width: 0, height: 7 },
    shadowRadius: 10,
    shadowOpacity: 0.2
  },
  productImage: {
    width: cardWidth - theme.SIZES.BASE,
    height: cardWidth - theme.SIZES.BASE,
    borderRadius: 3
  },
  productMap: {
    width: cardWidth - theme.SIZES.BASE,
    height: 200,
    borderRadius: 10,
    marginBottom:10

  },
  productPrice: {
    paddingTop: theme.SIZES.BASE,
    paddingBottom: theme.SIZES.BASE / 2
  },
  productDescription: {
    paddingTop: theme.SIZES.BASE
    // paddingBottom: theme.SIZES.BASE * 2,
  },
  marker: {
    width: 50,
    height: 50,
  },
  chipsScrollView: {
 
    top:Platform.OS === 'ios' ? 90 : 80, 
    paddingHorizontal:10
  },
  chipsIcon: {
    marginRight: 5,
  },
  chipsItem: {
    flexDirection:"row",
    backgroundColor:'#fff', 
    borderRadius:20,
    padding:8,
    paddingHorizontal:20, 
    marginHorizontal:10,
    height:35,
    shadowColor: '#ccc',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.5,
    shadowRadius: 5,
    elevation: 10,
  },

});

export default Articles;