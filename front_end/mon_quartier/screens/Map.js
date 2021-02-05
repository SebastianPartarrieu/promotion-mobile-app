
import React, { useEffect, useState } from 'react';
import {
  StyleSheet,
  Text,
  TextInput,
  View,
  ScrollView,
  Animated,
  Image,
  TouchableOpacity,
  Dimensions,
  Platform,
  Callout, Button, Block
} from "react-native";
import MapView, {Marker, PROVIDER_GOOGLE} from "react-native-maps";

import Ionicons from 'react-native-vector-icons/Ionicons';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import Fontisto from 'react-native-vector-icons/Fontisto'



//import articles from "../constants/articles";
import {sendSearchRequest} from "../navigation/Screens";
import {RetroStyle} from "../constants/MapData";
const { width, height } = Dimensions.get("window");
const CARD_HEIGHT = 220;
const CARD_WIDTH = width * 0.8;
const SPACING_FOR_CARD_INSET = width * 0.1 - 10;







 
 function Map ({navigation}){
  

  function MapUpdateFunction(response){
    { //console.log(response),
      articles = setArticles(response['resultat'])
      }
  }
  
  //var articles = props.KOM;

  //var [articles, setArticles] = useState(props.KOM);
  var [articles, setArticles] = useState([]);

  console.log(articles)

  function SearchResults(){
    /* 
      Retourne une liste de JSX Elements qui sont des markers correspondants au résultat de la recherche
      Les markers sont bien placés avec les coordonées.
    */
    //const scaleStyle = {transform: [{scale: interpolations[index].scale,},],}; pour rescale
    var buffer = [];
    var n = articles.length;

    for(var iter = 0; iter < n; iter++){

      const id = iter;
      buffer.push(<MapView.Marker key={id} coordinate={{latitude: articles[id][6], longitude: articles[id][7]}} onPress={(e)=>onMarkerPress(e)}><Animated.View style={[styles.markerWrap]}><Animated.Image source={require('../assets/imgs/pin.png')} style={[styles.marker, /* scaleStyle */]} resizeMode="contain"/></Animated.View></MapView.Marker>)
    }
    return(buffer)
  } 


  function SetEtiquettes(){
    /* 
      Retourne une liste de JSX Elements qui sont les slides en bas correspondants au résultat de la recherche
    */
    var buffer = [];
    var n = articles.length;
    for(var iter = 0; iter < n; iter++){
      const id = iter;
      buffer.push(
      <View style={styles.card} key={id} >

        <Image source={{uri: ''}} style={styles.cardImage} resizeMode="contain"/>
    
        <View style={styles.textContent}>
        <TouchableOpacity
          onPress = {() => navigation.navigate('Profile', {comm : articles[id]})}
          >
          <Text numberOfLines={1} style={styles.cardtitle}>{articles[id][1]}
          </Text>
          
          <Text numberOfLines={1} style={styles.cardDescription}>{articles[id][2]}
          </Text>
          </TouchableOpacity>
          </View>
          <View style={styles.button}>
          </View>
        
      </View>)

    }
    return(buffer)
  }



  const initialMapState = {
    articles,
    categories: [
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
  ],
    region: {
      //latitude: articles[0][6],
      //longitude: articles[0][7],
      latitude: 48.845770758284,    // la map s'initialise au coord de l'école des Mines, à changer avec les geoloc du tel.
      longitude: 2.338596411379499,
      latitudeDelta: 0.02864195044303443,
      longitudeDelta: 0.020142817690068,
    },
  };

  const [state, setState] = React.useState(initialMapState);

  let mapIndex = 0;
  let mapAnimation = new Animated.Value(0);

  useEffect(() => {
    mapAnimation.addListener(({ value }) => {
      let index = Math.floor(value / CARD_WIDTH + 0.3); // animate 30% away from landing on the next item
      if (index >= state.articles.length) {
        index = state.articles.length - 1;
      }
      if (index <= 0) {
        index = 0;
      }

      clearTimeout(regionTimeout);

      const regionTimeout = setTimeout(() => {
        if( mapIndex !== index ) {
          mapIndex = index;
          _map.current.animateToRegion(
            {
              latitude: state.articles[index][6],
              longitude: state.articles[index][7],
              latitudeDelta: state.region.latitudeDelta,
              longitudeDelta: state.region.longitudeDelta,
            },
            350
          );
        }
      }, 10);
    });
  });

  const interpolations = state.articles.map((marker, index) => {
    const inputRange = [
      (index - 1) * CARD_WIDTH,
      index * CARD_WIDTH,
      ((index + 1) * CARD_WIDTH),
    ];

    const scale = mapAnimation.interpolate({
      inputRange,
      outputRange: [1, 1.5, 1],
      extrapolate: "clamp"
    });

    return { scale };
  });

  const onMarkerPress = (mapEventData) => {
    const markerID = mapEventData._targetInst.return.key;

    let x = (markerID * CARD_WIDTH) + (markerID * 20); 
    if (Platform.OS === 'ios') {
      x = x - SPACING_FOR_CARD_INSET;
    }

    _scrollView.current.scrollTo({x: x, y: 0, animated: true});
  }

  const _map = React.useRef(null);
  const _scrollView = React.useRef(null);
  

  return (
    <View style={styles.container}>
      <MapView
        ref={_map}
        initialRegion={state.region}
        style={styles.container}
        provider={PROVIDER_GOOGLE}
        customMapStyle={RetroStyle}
        showsUserLocation={true}
        followsUserLocation={true}
      >
      
        
        
      <SearchResults/>

      </MapView>
      <View style={styles.searchBox}>
        <TextInput
          onChangeText = {(text) => (sendSearchRequest(text,MapUpdateFunction,"commerce"))}

          placeholder="Chercher des commerces"
          placeholderTextColor="#000"
          autoCapitalize="none"
          style={{flex:1,padding:0}}
        />
        <Ionicons name="ios-search" size={20} />
      </View>
      <ScrollView
        horizontal
        scrollEventThrottle={1}
        showsHorizontalScrollIndicator={false}
        height={50}
        style={styles.chipsScrollView}
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
        {state.categories.map((category, index) => (
          <TouchableOpacity key={index} style={styles.chipsItem}>
            {category.icon}
            <Text>{category.name}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>
      <Animated.ScrollView
        ref={_scrollView}
        horizontal
        pagingEnabled
        scrollEventThrottle={1}
        showsHorizontalScrollIndicator={false}
        snapToInterval={CARD_WIDTH + 20}
        snapToAlignment="center"
        style={styles.scrollView}
        contentInset={{
          top: 0,
          left: SPACING_FOR_CARD_INSET,
          bottom: 0,
          right: SPACING_FOR_CARD_INSET
        }}
        contentContainerStyle={{
          paddingHorizontal: Platform.OS === 'android' ? SPACING_FOR_CARD_INSET : 0
        }}
        onScroll={Animated.event(
          [
            {
              nativeEvent: {
                contentOffset: {
                  x: mapAnimation,
                }
              },
            },
          ],
          {useNativeDriver: true}
        )}
      >

      <SetEtiquettes/>
      </Animated.ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    //position: 'absolute',
    //justifyContent : 'flex-end',
    //alignItems : 'center',
    flex: 1,
  },
  searchBox: {
    position:'absolute', 
    marginTop: Platform.OS === 'ios' ? 40 : 20, 
    flexDirection:"row",
    backgroundColor: '#fff',
    width: '90%',
    alignSelf:'center',
    borderRadius: 5,
    padding: 10,
    shadowColor: '#ccc',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.5,
    shadowRadius: 5,
    elevation: 10,
  },
  chipsScrollView: {
    position:'absolute', 
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
  scrollView: {
    position: "absolute",
    bottom: 0,
    left: 0,
    right: 0,
    paddingVertical: 10,
  },
  endPadding: {
    paddingRight: width - CARD_WIDTH,
  },
  card: {
    // padding: 10,
    elevation: 5,
    backgroundColor: "#FFF",
    borderRadius:10,
    marginHorizontal: 10,
    shadowColor: "#000",
    shadowRadius: 10,
    shadowOpacity: 0.5,
    shadowOffset: { x: 2, y: -2 },
    height: CARD_HEIGHT,
    width: CARD_WIDTH,
    overflow: "hidden",
    marginBottom:20
  },
  cardImage: {
    flex: 4,
    width: "100%",
    height: "100%",
    alignSelf: "center",
    marginTop:10,
    borderRadius:5,
  },
  textContent: {
    flex: 1,
    padding: 10,
  },
  cardtitle: {
    fontSize: 12,
    // marginTop: 5,
    fontWeight: "bold",
  },
  cardDescription: {
    fontSize: 12,
    color: "#444",
  },
  markerWrap: {
    alignItems: "center",
    justifyContent: "center",
    width:80,
    height:80,
  },
  marker: {
    width: 50,
    height: 50,
  },
  button: {
    alignItems: 'flex-end',
    marginBottom: 10,
    marginRight: 5
  },
  signIn: {
      width: '100%',
      padding:5,
      justifyContent: 'center',
      alignItems: 'center',
      borderRadius: 3,
      marginBottom: 5
  },
  textSign: {
      fontSize: 15,

  }
});

export default Map;