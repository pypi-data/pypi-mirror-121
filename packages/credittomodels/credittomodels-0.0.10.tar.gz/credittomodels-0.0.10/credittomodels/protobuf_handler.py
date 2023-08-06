from credittomodels.Bid import Bid
from credittomodels.Offer import Offer
from credittomodels.Match import Match

from credittomodels import creditto_models_pb2 as CredittoModelsProto
from google.protobuf import message as _message


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
        try:
            received_proto_bid = CredittoModelsProto.Bid()
            received_proto_bid.ParseFromString(bid_dta)

            # Extracting data from deserialized bid and creating a new Bid instance
            received_bid = Bid(received_proto_bid.id, received_proto_bid.owner_id, received_proto_bid.bid_interest,
                               received_proto_bid.target_offer_id, received_proto_bid.partial_only,
                               received_proto_bid.partial_sum, received_proto_bid.date_added, received_proto_bid._status)

            return received_bid

        except _message.DecodeError as e:
            print(f"Provided input can't be deserialized to a Bid: {e}")
            return False

        except Exception as e:
            print(f"Deserialization error: {e}")
            return -1

    @staticmethod
    def serialize_offer_to_proto(offer: Offer):
        """
        This method can be used to convert an Offer instance to serialized Data Transfer Object, google protobuf message.
        :param offer: Valid Offer instance
        :return: array of bytes, serialized  google protobuf message
        """

        serialized_offer = CredittoModelsProto.Offer()

        serialized_offer.id = offer.id
        serialized_offer.type = offer.type
        serialized_offer.owner_id = offer.owner_id

        serialized_offer.sum = offer.sum
        serialized_offer.duration = offer.duration
        serialized_offer.offered_interest = offer.offered_interest

        serialized_offer.allow_partial_fill = offer.allow_partial_fill
        serialized_offer.date_added = offer.date_added
        serialized_offer._status = offer.status

        serialized_offer.matching_bid = offer.matching_bid
        serialized_offer.final_interest = offer.final_interest

        return serialized_offer.SerializeToString()

    @staticmethod
    def deserialize_proto_to_offer(offer_dta):
        """
        This method can be used to convert serialized Data Transfer Object, google protobuf message to Offer instance
        :param offer_dta: array of bytes, serialized Date Transfer Object, Offer protobuf message
        :return: Offer instance
        """
        try:
            received_proto_offer = CredittoModelsProto.Offer()
            received_proto_offer.ParseFromString(offer_dta)

            # Extracting data from deserialized bid and creating a new Offer instance
            received_offer = Offer(received_proto_offer.id, received_proto_offer.owner_id, received_proto_offer.sum,
                                 received_proto_offer.duration, received_proto_offer.offered_interest,
                                 received_proto_offer.allow_partial_fill, received_proto_offer.date_added,
                                 received_proto_offer._status)

            received_offer.matching_bid = received_proto_offer.matching_bid
            received_offer.final_interest = received_proto_offer.final_interest

            return received_offer

        except _message.DecodeError as e:
            print(f"Provided input can't be deserialized to an Offer: {e}")
            return False

        except Exception as e:
            print(f"Deserialization error: {e}")
            return -1

    @staticmethod
    def serialize_match_to_proto(match: Match):
        """
        This method can be used to convert a Match instance to serialized Data Transfer Object, google protobuf message.
        :param match: Valid Match instance
        :return: array of bytes, serialized  google protobuf message
        """

        serialized_match = CredittoModelsProto.Match()

        serialized_match.id = match.id
        serialized_match.type = match.type
        serialized_match.offer_id = match.offer_id

        serialized_match.bid_id = match.bid_id
        serialized_match.offer_owner_id = match.offer_owner_id
        serialized_match.bid_owner_id = match.bid_owner_id

        serialized_match.match_time = match.match_time
        serialized_match.partial = match.partial
        serialized_match.final_interest = match.final_interest

        serialized_match.monthly_payment = match.monthly_payment

        return serialized_match.SerializeToString()

    @staticmethod
    def deserialize_proto_to_match(match_dta):
        """
        This method can be used to convert serialized Data Transfer Object, google protobuf message to Match instance
        :param match_dta: array of bytes, serialized Date Transfer Object, Offer protobuf message
        :return: Match instance
        """
        try:
            received_proto_match = CredittoModelsProto.Match()
            received_proto_match.ParseFromString(match_dta)

            # Extracting data from deserialized bid and creating a new Match instance
            received_match = Match(received_proto_match.offer_id, received_proto_match.bid_id,
                                   received_proto_match.offer_owner_id, received_proto_match.bid_owner_id,
                                   received_proto_match.match_time, received_proto_match.partial,
                                   received_proto_match.final_interest, received_proto_match.monthly_payment)

            return received_match

        except _message.DecodeError as e:
            print(f"Provided input can't be deserialized to a Match: {e}")
            return False

        except Exception as e:
            print(f"Deserialization error: {e}")
            return -1





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
#     c = b'ffdef'
#
#     print(ProtoHandler.deserialize_proto_to_bid(c))