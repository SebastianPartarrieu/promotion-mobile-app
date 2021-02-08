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
  Button
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

import server from "../constants/Server";



const { width } = Dimensions.get("screen");

const thumbMeasure = (width - 48 - 32) / 3;
const cardWidth = width - theme.SIZES.BASE * 2;



function sendArticlesRequest(updateFunction,route){
  const url = new URL(route, server.server)

  fetch(url, {
    method : 'GET'
  }).then((response) => response.json()).then(updateFunction).catch(
    (e) => {alert('Something went wrong' + e.message)}
  )
}

var k=0;


function Articles(props) {

    var [articles, setArticles] = React.useState([])
    var [images, setImages] = useState([])
    

    function updateFunction(response){
      { 
        articles = setArticles(response['resultat'])
        images = setImages(response['images'])
        
        }
    }
    k=1;
 
    
    useEffect( ()=>{sendArticlesRequest(updateFunction, "commerce");}, []);

 if (articles.length == 0 ) {
  
  return(
      <Block center>
        <Text>pas d'articles</Text>
      </Block>
        )}

    //console.log(articles)
    var i = 0;
    var suggestions = [];
    //while(i<6){suggestions.push(articles[i]), i+=1};

    function Suggest(){
      var buffer = [];
      //var n = resultat.length;
      var n = 3;

      for(var iter = 0; iter < n; iter++){
  
        const id = iter;
        buffer.push(
          <Block style={styles.productItem} >     
            <Card item={articles[id]} im ={images[id]} full />
          </Block>
        )
      }
      return(buffer)
    }

    function SmallSlide(){
      var buffer = [];
      var n = articles.length;
  
      for(var iter = 0; iter < n; iter++){

      const id = iter;
      buffer.push(
      <Block style={styles.productScroll}>
        <Card 
          item={articles[id]}
          im = {images[id]}/>
      </Block>)
      }
      return(buffer)
    }


    const { navigation } = props;
    const categories= [
      { 
        name: 'Fastfood', 
        icon: <MaterialCommunityIcons style={styles.chipsIcon} name="food-fork-drink" size={18} />,
      },
      {
        name: 'Restaurant',
        icon: <Ionicons name="ios-restaurant" style={styles.chipsIcon} size={18} />,
      },
      {
        name: 'Coiffeurs',
        icon: <Ionicons name="md-restaurant" style={styles.chipsIcon} size={18} />,
      },
      {
        name: 'Magasin',
        icon: <MaterialCommunityIcons name="food" style={styles.chipsIcon} size={18} />,
      },
      {
        name: 'Hotel',
        icon: <Fontisto name="hotel" style={styles.chipsIcon} size={15} />,
      },
    ]
    
    return (
      <Block flex center>
        <ScrollView
          showsVerticalScrollIndicator={false}
        >
        <Block flex style={styles.group}>
        
        <Text bold size={16} style={styles.title}>
          Suggestions
        </Text>
        <Block flex >
            <ScrollView
              horizontal={true}
              pagingEnabled={true}
              decelerationRate={0}
              scrollEventThrottle={16}
              snapToAlignment="center"
              showsHorizontalScrollIndicator={true}
              snapToInterval={cardWidth + theme.SIZES.BASE * 0.375}
              contentContainerStyle={{
              paddingHorizontal: theme.SIZES.BASE / 2
              }}
            >
            <Suggest/>
            </ScrollView>
          </Block>
          <Text bold size={16} style={styles.title}>
          Autour de vous
        </Text>
          <Block flex center>
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
                  <MapView.Marker key={index} coordinate={{latitude: marker[6], longitude: marker[7]}}>
                    <Image
                      source={require('../assets/imgs/pin.png')}
                      style={styles.marker}
                      resizeMode="contain"
                    />
                </MapView.Marker>
                );
              })}
            </MapView>
            </Block>
            <Text bold size={26} style={styles.title}>
          Catégories
        </Text>
        <Block flex>
            <ScrollView
            horizontal
            scrollEventThrottle={1}
            showsHorizontalScrollIndicator={false}
            height={50}
          //  style={styles.chipsScrollView}
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
            {categories.map((category, index) => (
              <TouchableOpacity key={index} style={styles.chipsItem}>
                {category.icon}
                <Text>{category.name}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </Block>
        <Block flex>
            <ScrollView
            horizontal
            scrollEventThrottle={1}
            showsHorizontalScrollIndicator={false}
         
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
            <SmallSlide/>
          </ScrollView>
        </Block>
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
    marginTop: 22,
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
    borderRadius: 10

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