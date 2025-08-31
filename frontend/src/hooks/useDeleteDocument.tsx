// src/hooks/useDeleteDocument.ts
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "../lib/apiFetch";
import toast from "react-hot-toast";

const deleteDocumentApi = async (docId: string) => {
  const response = await apiFetch.delete(`/documents/${docId}`);
  return response.data;
};

export const useDeleteDocument = (options?: { onSuccess?: () => void }) => {
  const queryClient = useQueryClient();

  const {
    mutate: deleteDocument,
    isPending: isDeleting,
  } = useMutation({
    mutationFn: deleteDocumentApi,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["documents"] });
      toast.success("Document deleted successfully.");
      
      if (options?.onSuccess) {
        options.onSuccess();
      }
    },
    onError: () => {
      toast.error("Failed to delete document.");
    },
  });

  return {
    deleteDocument,
    isDeleting,
  };
};