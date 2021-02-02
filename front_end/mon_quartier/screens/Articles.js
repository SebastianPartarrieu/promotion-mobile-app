import React from "react";
import {
  ScrollView,
  StyleSheet,
  Image,
  TouchableWithoutFeedback,
  ImageBackground,
  Dimensions,
  View
} from "react-native";
//galio
import { Block, Text, theme } from "galio-framework";
//argon
import { articles, Images, argonTheme } from "../constants/";
import { Card } from "../components/";
import MapView, {Marker, PROVIDER_GOOGLE} from "react-native-maps";
import {RetroStyle} from "../constants/MapData";


const { width } = Dimensions.get("screen");

const thumbMeasure = (width - 48 - 32) / 3;
const cardWidth = width - theme.SIZES.BASE * 2;
const categories = [
  {
    title: "Panda WOK",
    description:
      "Jap a volonté pas cher",
    image:
      "data:image/jpeg;base64,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",
    price: "0.2 km"
  },
  {
    title: "MyAuchan",
    description:
      "Rock music is a genre of popular music. It developed during and after the 1960s in the United Kingdom.",
    image:
      "https://www.pagesjaunes.fr/media/vignette/AAA0RFO3X2QZ-V73000.gif",
    price: "0.1 km"
  },
  {
    title: "NYAN CAT",
    description:
      "Rock music is a genre of popular music. It developed during and after the 1960s in the United Kingdom.",
    image:
      "https://f.hellowork.com/blogdumoderateur/2013/02/gif-anime.gif",
    price: "$35"
  }
];

var i = 0;
var suggestions = [];
while(i<3){suggestions.push(articles[i]), i+=1};

class Articles extends React.Component {
  renderSearch = () => {
    const { navigation } = this.props;
    return (
      <Input
        right
        color="black"
        style={styles.search}
        placeholder="What are you looking for?"
        placeholderTextColor={'#8898AA'}
        onFocus={() => navigation.navigate('Pro')}
        iconContent={<Icon size={16} color={theme.COLORS.MUTED} name="search-zoom-in" family="ArgonExtra" />}
      />
    );
  }
  renderProduct = (item, index) => {
    const { navigation } = this.props;

    return (
      <TouchableWithoutFeedback
        style={{ zIndex: 3 }}
        key={"product-${item.nom}"}
        onPress={() => navigation.navigate("Profile", { item: item })}
      >
        <Block center style={styles.productItem}>
          <Image
            resizeMode="contain"
            style={styles.productImage}
            source={{ uri: item.image }}
          />
          <Block center style={{ paddingHorizontal: theme.SIZES.BASE }}>
            <Text
              center
              size={16}
              color={theme.COLORS.MUTED}
              style={styles.productPrice}
            >
              {item.adresse}
            </Text>
            <Text center size={34}>
              {item.nom}
            </Text>
            <Text
              center
              size={16}
              color={theme.COLORS.MUTED}
              style={styles.productDescription}
            >
              {item.description}
            </Text>
          </Block>
        </Block>
      </TouchableWithoutFeedback>
    );
  };

  renderCards = () => {
    const { navigation } = this.props;
    return (
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
              {categories &&
                suggestions.map((item, index) =>
                <Block style={styles.productItem}>
                  <Card item={item} full/>
                </Block>
                )}
            </ScrollView>
          </Block>
          <Text bold size={16} style={styles.title}>
          Autour de vous
        </Text>
          <Block flex center>
            <MapView
              initialRegion={{
                latitude: articles[0].coordinates.latitude,
                longitude: articles[0].coordinates.longitude,
                latitudeDelta: 0.02864195044303443,
                longitudeDelta: 0.020142817690068,
              }}
              provider={PROVIDER_GOOGLE}
              customMapStyle={RetroStyle}
              style={styles.productMap}
              onPress={() => navigation.navigate('Map')}
              showsUserLocation={true}
              followsUserLocation={true}
            >
              {articles.map((marker, index) => {
            
                return (
                  <MapView.Marker key={index} coordinate={{latitude: marker.coordinates.latitude, longitude: marker.coordinates.longitude}}>
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
          <Block style={{ paddingHorizontal: theme.SIZES.BASE }}>
            <Card item={articles[0]} horizontal />
            <Block flex row>
              <Card
                item={articles[1]}
                style={{ marginRight: theme.SIZES.BASE }}
              />
              <Card item={articles[2]} />
            </Block>
            <Card item={articles[4]} full />
           
          </Block>
          
        </Block>
      </Block>
    );
  };


  renderHeader = () => {
    const { search, options, tabs } = this.props;
    if (search || tabs || options) {
      return (
        <Block center>
          {search ? this.renderSearch() : null}
          {options ? this.renderOptions() : null}
          {tabs ? this.renderTabs() : null}
        </Block>
      );
    }
  }

  render() {
    return (
      <Block flex center>
        <ScrollView
          showsVerticalScrollIndicator={false}
        >
          {this.renderCards()}
    
        </ScrollView>
      </Block>
    );
  }
}

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
    height: 50,},

});

export default Articles;
