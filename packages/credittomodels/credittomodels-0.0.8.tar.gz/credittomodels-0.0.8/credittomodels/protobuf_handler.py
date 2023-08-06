from credittomodels.Bid import Bid
from credittomodels import creditto_models_pb2 as CredittoModelsProto


class ProtoHandler:

    @staticmethod
    def serialize_bid_to_proto(bid: Bid):
        """
        This method can be used to convert a Bid instance to serialized Data Transfer Object, google protobuf message.
        :param bid: Valid Bid instance
        :return: array of bytes, serialized  google protobuf message
        """

        serialized_bid = CredittoModelsProto.Bid()

        serialized_bid.id = bid.id
        serialized_bid.type = bid.type
        serialized_bid.owner_id = bid.owner_id

        serialized_bid.bid_interest = bid.bid_interest
        serialized_bid.target_offer_id = bid.target_offer_id
        serialized_bid.partial_only = bid.partial_only

        serialized_bid.partial_sum = bid.partial_sum
        serialized_bid.date_added = bid.date_added
        serialized_bid._status = bid.status

        return serialized_bid.SerializeToString()

    @staticmethod
    def deserialize_proto_to_bid(bid_dta):
        """
        This method can be used to convert serialized Data Transfer Object, google protobuf message to Bid instance
        :param bid_dta: array of bytes, serialized Date Transfer Object, Bid protobuf message
        :return: Bid instance
        """
        received_proto_bid = CredittoModelsProto.Bid()
        received_proto_bid.ParseFromString(bid_dta)

        # Extracting data from deserialized bid and creating a new Bid instance
        received_bid = Bid(received_proto_bid.id, received_proto_bid.owner_id, received_proto_bid.bid_interest,
                           received_proto_bid.target_offer_id, received_proto_bid.partial_only,
                           received_proto_bid.partial_sum, received_proto_bid.date_added, received_proto_bid._status)

        return received_bid


# if __name__ == '__main__':
#     id = 12
#     owner_id = 912
#     bid_interest = 0.07
#     target_offer_id = 34
#     partial_only = 0
#
#     # Creating a Bid instance
#     raw_bid = Bid(id, owner_id, bid_interest, target_offer_id, partial_only)
#     a = ProtoHandler.serialize_bid_to_proto(raw_bid)
#
#     print(ProtoHandler.deserialize_proto_to_bid(a))