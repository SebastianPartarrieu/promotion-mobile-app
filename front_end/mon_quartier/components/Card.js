import React from 'react';
import { withNavigation } from '@react-navigation/compat';
import PropTypes from 'prop-types';
import { StyleSheet, Dimensions, Image, TouchableWithoutFeedback } from 'react-native';
import { Block, Text, theme } from 'galio-framework';
import Profile from '../screens/Profile';
import { argonTheme } from '../constants';
import { articles } from '../constants';

class Card extends React.Component {
  render() {
    const { navigation, item,im, horizontal, full, style, ctaColor, imageStyle } = this.props;


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
        <TouchableWithoutFeedback o onPress = {() => navigation.navigate('Profile', {comm : item, imm:im})}>
          <Block flex style={imgContainer}>
            <Image source={{uri: 'http://localhost:5000/' + im[0] }} style={imageStyles} resizeMode="contain"/>
          </Block>
        </TouchableWithoutFeedback>
        <TouchableWithoutFeedback  onPress = {() => navigation.navigate('Profile', {comm : item, imm:im})}>
          <Block flex space="between" style={styles.cardDescription}>
            <Text bold center size={15} style={styles.cardTitle}>{item[1]}</Text>
            <Text numberOfLines={1} style={styles.cardDescription}>{item[2]}</Text>
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
    minHeight: 50,
    marginBottom: 16,
    borderRadius: 10,
  },
  cardTitle: {
    flex: 1,
    flexWrap: 'wrap',
    marginTop:5

  },
  imageContainer: {
    borderRadius: 10,
    elevation: 1,
    overflow: 'hidden',
    margin: 10
    
  },
  image: {
    // borderRadius: 3,
    margin: 10
  },
  horizontalImage: {
    height: 50,
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
  cardDescription: {
    fontSize: 8,
    color: "#444",
    margin:5
  }
});

export default withNavigation(Card);