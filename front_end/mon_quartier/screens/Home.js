import React from 'react';
import { StyleSheet, Dimensions, ScrollView } from 'react-native';
import { Block, theme } from 'galio-framework';
import Map from '../screens/Map';
import { Card } from '../components';
import articles from '../constants/articles';
import { token } from './Onboarding';
import Onboarding from './Onboarding';
const { width } = Dimensions.get('screen');

function Accueil () {

    return (
      <Block flex center style={styles.home}>
        <Text>W
        </Text>
      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.articles}>
        <Block flex>
          <Card item={articles[0]} horizontal  />
          <Block flex row>
            <Card item={articles[1]} style={{ marginRight: theme.SIZES.BASE }} />
            <Card item={articles[2]} />
          </Block>
          <Block>
            <Map item = {csvjson[0].coordinates}/>
          </Block>
          <Card item={articles[3]} horizontal />
          <Card item={articles[4]} full />
        </Block>
      </ScrollView>
      </Block>
    )
  }


const styles = StyleSheet.create({
  home: {
    width: width,    
  },
  articles: {
    width: width - theme.SIZES.BASE * 2,
    paddingVertical: theme.SIZES.BASE,
  },
});

export default Accueil;
