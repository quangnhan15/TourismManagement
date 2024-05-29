import { View, Text, ActivityIndicator } from "react-native"
import MyStyles from "../../styles/MyStyles"
import Styles from "./Styles"
import { useEffect, useState } from "react"
import API, { endpoints } from "../../configs/API"

const Home = () => {
    const [tours, setTours] = useState(null)

    useEffect(() => {
        const loadTours = async () => {
            try {
                let res = await API.get(endpoints['tours']);
                setTours(res.data.results)
                res.data
            } catch (ex) {
                console.error(ex);
            }
        }

        loadTours();
    }, []);

    return (
        <View style={MyStyles.container}>
            <Text style={Styles.subject}>HOME</Text>
            {tours===null?<ActivityIndicator/>:<>
                {tours.map(c => (
                    <View key={c.id}>
                        <Text>{c.tour_name}</Text>
                    </View>
                ))}
            </>}
        </View>
    )
}
export default Home