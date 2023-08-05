# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from exa.module_repository_pb import module_repository_pb2 as exa_dot_module__repository__pb_dot_module__repository__pb2


class ModuleRepositoryStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterObject = channel.unary_unary(
                '/exa.module_repository_pb.ModuleRepository/RegisterObject',
                request_serializer=exa_dot_module__repository__pb_dot_module__repository__pb2.RegisterObjectRequest.SerializeToString,
                response_deserializer=exa_dot_module__repository__pb_dot_module__repository__pb2.RegisterObjectResponse.FromString,
                )
        self.GetObjectMetadata = channel.unary_unary(
                '/exa.module_repository_pb.ModuleRepository/GetObjectMetadata',
                request_serializer=exa_dot_module__repository__pb_dot_module__repository__pb2.GetObjectMetadataRequest.SerializeToString,
                response_deserializer=exa_dot_module__repository__pb_dot_module__repository__pb2.GetObjectMetadataResponse.FromString,
                )
        self.GetObjectIdFromTag = channel.unary_unary(
                '/exa.module_repository_pb.ModuleRepository/GetObjectIdFromTag',
                request_serializer=exa_dot_module__repository__pb_dot_module__repository__pb2.GetObjectIdFromTagRequest.SerializeToString,
                response_deserializer=exa_dot_module__repository__pb_dot_module__repository__pb2.GetObjectIdFromTagResponse.FromString,
                )
        self.AddTagForObjectId = channel.unary_unary(
                '/exa.module_repository_pb.ModuleRepository/AddTagForObjectId',
                request_serializer=exa_dot_module__repository__pb_dot_module__repository__pb2.AddTagForObjectIdRequest.SerializeToString,
                response_deserializer=exa_dot_module__repository__pb_dot_module__repository__pb2.AddTagForObjectIdResponse.FromString,
                )
        self.RegisterBlob = channel.unary_unary(
                '/exa.module_repository_pb.ModuleRepository/RegisterBlob',
                request_serializer=exa_dot_module__repository__pb_dot_module__repository__pb2.RegisterBlobRequest.SerializeToString,
                response_deserializer=exa_dot_module__repository__pb_dot_module__repository__pb2.RegisterBlobResponse.FromString,
                )
        self.GetBlob = channel.unary_stream(
                '/exa.module_repository_pb.ModuleRepository/GetBlob',
                request_serializer=exa_dot_module__repository__pb_dot_module__repository__pb2.GetBlobRequest.SerializeToString,
                response_deserializer=exa_dot_module__repository__pb_dot_module__repository__pb2.GetBlobResponse.FromString,
                )
        self.ExistsBlob = channel.unary_unary(
                '/exa.module_repository_pb.ModuleRepository/ExistsBlob',
                request_serializer=exa_dot_module__repository__pb_dot_module__repository__pb2.ExistsBlobRequest.SerializeToString,
                response_deserializer=exa_dot_module__repository__pb_dot_module__repository__pb2.ExistsBlobResponse.FromString,
                )
        self.ClearData = channel.unary_unary(
                '/exa.module_repository_pb.ModuleRepository/ClearData',
                request_serializer=exa_dot_module__repository__pb_dot_module__repository__pb2.ClearDataRequest.SerializeToString,
                response_deserializer=exa_dot_module__repository__pb_dot_module__repository__pb2.ClearDataResponse.FromString,
                )


class ModuleRepositoryServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RegisterObject(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetObjectMetadata(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetObjectIdFromTag(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddTagForObjectId(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RegisterBlob(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBlob(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ExistsBlob(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClearData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ModuleRepositoryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RegisterObject': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterObject,
                    request_deserializer=exa_dot_module__repository__pb_dot_module__repository__pb2.RegisterObjectRequest.FromString,
                    response_serializer=exa_dot_module__repository__pb_dot_module__repository__pb2.RegisterObjectResponse.SerializeToString,
            ),
            'GetObjectMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.GetObjectMetadata,
                    request_deserializer=exa_dot_module__repository__pb_dot_module__repository__pb2.GetObjectMetadataRequest.FromString,
                    response_serializer=exa_dot_module__repository__pb_dot_module__repository__pb2.GetObjectMetadataResponse.SerializeToString,
            ),
            'GetObjectIdFromTag': grpc.unary_unary_rpc_method_handler(
                    servicer.GetObjectIdFromTag,
                    request_deserializer=exa_dot_module__repository__pb_dot_module__repository__pb2.GetObjectIdFromTagRequest.FromString,
                    response_serializer=exa_dot_module__repository__pb_dot_module__repository__pb2.GetObjectIdFromTagResponse.SerializeToString,
            ),
            'AddTagForObjectId': grpc.unary_unary_rpc_method_handler(
                    servicer.AddTagForObjectId,
                    request_deserializer=exa_dot_module__repository__pb_dot_module__repository__pb2.AddTagForObjectIdRequest.FromString,
                    response_serializer=exa_dot_module__repository__pb_dot_module__repository__pb2.AddTagForObjectIdResponse.SerializeToString,
            ),
            'RegisterBlob': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterBlob,
                    request_deserializer=exa_dot_module__repository__pb_dot_module__repository__pb2.RegisterBlobRequest.FromString,
                    response_serializer=exa_dot_module__repository__pb_dot_module__repository__pb2.RegisterBlobResponse.SerializeToString,
            ),
            'GetBlob': grpc.unary_stream_rpc_method_handler(
                    servicer.GetBlob,
                    request_deserializer=exa_dot_module__repository__pb_dot_module__repository__pb2.GetBlobRequest.FromString,
                    response_serializer=exa_dot_module__repository__pb_dot_module__repository__pb2.GetBlobResponse.SerializeToString,
            ),
            'ExistsBlob': grpc.unary_unary_rpc_method_handler(
                    servicer.ExistsBlob,
                    request_deserializer=exa_dot_module__repository__pb_dot_module__repository__pb2.ExistsBlobRequest.FromString,
                    response_serializer=exa_dot_module__repository__pb_dot_module__repository__pb2.ExistsBlobResponse.SerializeToString,
            ),
            'ClearData': grpc.unary_unary_rpc_method_handler(
                    servicer.ClearData,
                    request_deserializer=exa_dot_module__repository__pb_dot_module__repository__pb2.ClearDataRequest.FromString,
                    response_serializer=exa_dot_module__repository__pb_dot_module__repository__pb2.ClearDataResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'exa.module_repository_pb.ModuleRepository', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ModuleRepository(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RegisterObject(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exa.module_repository_pb.ModuleRepository/RegisterObject',
            exa_dot_module__repository__pb_dot_module__repository__pb2.RegisterObjectRequest.SerializeToString,
            exa_dot_module__repository__pb_dot_module__repository__pb2.RegisterObjectResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetObjectMetadata(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exa.module_repository_pb.ModuleRepository/GetObjectMetadata',
            exa_dot_module__repository__pb_dot_module__repository__pb2.GetObjectMetadataRequest.SerializeToString,
            exa_dot_module__repository__pb_dot_module__repository__pb2.GetObjectMetadataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetObjectIdFromTag(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exa.module_repository_pb.ModuleRepository/GetObjectIdFromTag',
            exa_dot_module__repository__pb_dot_module__repository__pb2.GetObjectIdFromTagRequest.SerializeToString,
            exa_dot_module__repository__pb_dot_module__repository__pb2.GetObjectIdFromTagResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddTagForObjectId(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exa.module_repository_pb.ModuleRepository/AddTagForObjectId',
            exa_dot_module__repository__pb_dot_module__repository__pb2.AddTagForObjectIdRequest.SerializeToString,
            exa_dot_module__repository__pb_dot_module__repository__pb2.AddTagForObjectIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RegisterBlob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exa.module_repository_pb.ModuleRepository/RegisterBlob',
            exa_dot_module__repository__pb_dot_module__repository__pb2.RegisterBlobRequest.SerializeToString,
            exa_dot_module__repository__pb_dot_module__repository__pb2.RegisterBlobResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBlob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/exa.module_repository_pb.ModuleRepository/GetBlob',
            exa_dot_module__repository__pb_dot_module__repository__pb2.GetBlobRequest.SerializeToString,
            exa_dot_module__repository__pb_dot_module__repository__pb2.GetBlobResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ExistsBlob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exa.module_repository_pb.ModuleRepository/ExistsBlob',
            exa_dot_module__repository__pb_dot_module__repository__pb2.ExistsBlobRequest.SerializeToString,
            exa_dot_module__repository__pb_dot_module__repository__pb2.ExistsBlobResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ClearData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exa.module_repository_pb.ModuleRepository/ClearData',
            exa_dot_module__repository__pb_dot_module__repository__pb2.ClearDataRequest.SerializeToString,
            exa_dot_module__repository__pb_dot_module__repository__pb2.ClearDataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
