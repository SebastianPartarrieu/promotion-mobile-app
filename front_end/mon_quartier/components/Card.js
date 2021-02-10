import React, {useState} from 'react';
import { withNavigation } from '@react-navigation/compat';
import PropTypes from 'prop-types';
import { StyleSheet,Image, TouchableWithoutFeedback } from 'react-native';
import { Block, Text, theme } from 'galio-framework';



import server from "../constants/Server";

class Card extends React.Component {
  render() {
    const { navigation, item, im, distance, horizontal, full, style, ctaColor, imageStyle } = this.props;


    const imageStyles = [
      full ? styles.fullImage : styles.horizontalImage,
      imageStyle
    ];
    const cardContainer = [styles.card, styles.shadow, style];
    const imgContainer = [styles.imageContainer,
      horizontal ? styles.horizontalStyles : styles.verticalStyles,
      styles.shadow
    ];
   
    if (im != undefined){
    return (
      <Block row={horizontal} card flex style={cardContainer}>
        <TouchableWithoutFeedback onPress = {() => navigation.navigate('Profile', {comm : item, imm:im})}>
          <Block flex style={imgContainer}>
            <Image source={{uri: server.server + im[0] }} style={imageStyles} resizeMode="contain"/>
          </Block>
        </TouchableWithoutFeedback>
        <TouchableWithoutFeedback  onPress = {() => navigation.navigate('Profile', {comm : item, imm:im})}>
          <Block flex space="between">
            <Text numberOfLines={1} bold center size={15} style={horizontal?styles.cardHorizontalTitle : styles.cardTitle}>{item[1]}</Text>
            <Text numberOfLines={1} italic center size={10} style={horizontal?styles.cardHorizontalDist : styles.cardDist}>à {distance} km</Text>
            <Text numberOfLines={1} style={full ? styles.fullcardDescription : styles.cardDescription}>{item[2]}</Text>
          </Block>
        </TouchableWithoutFeedback>
      </Block>
    )}
    else {
    return(<Block></Block>);
  }
  }
}

Card.propTypes = {
  item: PropTypes.any,
  horizontal: PropTypes.bool,
  full: PropTypes.bool,
  ctaColor: PropTypes.string,
  imageStyle: PropTypes.any,
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: theme.COLORS.WHITE,
    marginVertical: theme.SIZES.BASE,
    borderWidth: 0,
    //minHeight: 40,
    marginBottom: 16,
    borderRadius: 10,
  },
  cardTitle: {
    flex: 5,
    flexWrap: 'wrap',
    marginTop:5,
    marginHorizontal:5

  },
  cardHorizontalTitle: {
    flex: 5,
    flexWrap: 'wrap',
    marginTop:15,
    marginHorizontal:5

  },
  cardDist: {
    flex: 5,
    flexWrap: 'wrap',
    marginTop:2,
    marginHorizontal:5

  },
  cardHorizontalDist: {
    flex: 5,
    flexWrap: 'wrap',
    marginTop:10,
    marginHorizontal:5,
    color: theme.COLORS.WHITE,

  },
  imageContainer: {
    borderRadius: 10,
    elevation: 4,
   // overflow: 'hidden',
    margin: 10
    
  },
  image: {
    // borderRadius: 3,
    margin: 0
  },
  horizontalImage: {
    height: 70,
    width: 'auto',
    
  },
  horizontalStyles: {
    borderTopRightRadius: 0,
    borderBottomRightRadius: 0,
  },
  verticalStyles: {
    borderBottomRightRadius: 0,
    borderBottomLeftRadius: 0
  },
  fullImage: {
    height: 150
  },
  shadow: {
    shadowColor: theme.COLORS.BLACK,
    shadowOffset: { width: 0, height: 2 },
    shadowRadius: 4,
    shadowOpacity: 0.1,
    elevation: 2,
  },
  fullcardDescription: {
    fontSize: 8,
    color: "#444",
    marginHorizontal: 5,
    //marginTop:15,
    marginBottom:10
  },
  cardDescription: {
    fontSize: 8,
    color: "#444",
    marginHorizontal: 5,
    marginTop:5,
    marginBottom:10
  }
});

export default withNavigation(Card);